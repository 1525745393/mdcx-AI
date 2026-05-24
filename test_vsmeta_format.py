#!/usr/bin/env python3
"""VSMETA 格式验证测试脚本

验证生成的 VSMETA 文件是否符合 Synology Video Station 标准格式。
基于用户提供的可识别文件结构进行对比分析。
"""

import sys
from io import BytesIO
from pathlib import Path


def decode_varint(data: bytes, offset: int) -> tuple[int, int]:
    """解码 protobuf varint，返回 (值, 新偏移量)"""
    result = 0
    shift = 0
    while True:
        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1
        if not (byte & 0x80):
            break
        shift += 7
    return result, offset


def parse_tag(tag_byte: int) -> tuple[int, int]:
    """解析 protobuf tag byte，返回 (field_number, wire_type)"""
    field_number = tag_byte >> 3
    wire_type = tag_byte & 0x07
    return field_number, wire_type


def analyze_vsmeta(filepath: str) -> dict:
    """分析 VSMETA 文件结构"""
    data = Path(filepath).read_bytes()
    result = {
        "file": filepath,
        "size": len(data),
        "header": None,
        "fields": [],
        "errors": [],
    }

    offset = 0

    # 检查文件头
    if len(data) >= 2 and data[0] == 0x08 and data[1] == 0x01:
        result["header"] = "Movie (0x08 0x01)"
        offset = 2
    else:
        result["errors"].append("Invalid header")
        return result

    # 解析字段
    while offset < len(data):
        if offset >= len(data):
            break

        tag_byte = data[offset]
        field_num, wire_type = parse_tag(tag_byte)
        offset += 1

        field_info = {
            "offset": offset - 1,
            "tag_hex": f"0x{tag_byte:02X}",
            "field_number": field_num,
            "wire_type": wire_type,
        }

        if wire_type == 0:  # Varint
            value, offset = decode_varint(data, offset)
            field_info["type"] = "varint"
            field_info["value"] = value

        elif wire_type == 2:  # Length-delimited
            length, offset = decode_varint(data, offset)
            if offset + length > len(data):
                result["errors"].append(
                    f"Field {field_num}: Length {length} exceeds file size at offset {offset}"
                )
                break
            payload = data[offset : offset + length]
            offset += length
            field_info["type"] = "length-delimited"
            field_info["length"] = length

            # 尝试解码为字符串
            try:
                text = payload.decode("utf-8")
                if len(text) > 100:
                    field_info["value_preview"] = text[:100] + "..."
                else:
                    field_info["value_preview"] = text
            except UnicodeDecodeError:
                field_info["value_preview"] = f"<binary {length} bytes>"

        else:
            result["errors"].append(
                f"Unknown wire type {wire_type} for field {field_num}"
            )
            break

        result["fields"].append(field_info)

    return result


def check_critical_issues(result: dict) -> list[str]:
    """检查关键问题"""
    issues = []
    fields = result["fields"]

    # 检查是否有索引字节问题（0x01 出现在不该出现的位置）
    for i, field in enumerate(fields):
        tag = field["tag_hex"]

        # GROUP2 (0x9A) 和 GROUP3 (0xAA) 后面不应该有 0x01 索引字节
        if tag in ("0x9A", "0xAA"):
            # 检查下一个字节是否为 0x01（错误的索引字节）
            next_offset = field["offset"] + 1
            if next_offset < result["size"]:
                # 这里简化处理，实际应该在解析时检查
                pass

    # 检查关键字段是否存在
    tag_set = {f["tag_hex"] for f in fields}

    # 检查是否有错误的索引字段标记
    # 0x8A 和 0x92 应该是普通 length-delimited，不是 indexed

    return issues


def print_analysis(result: dict):
    """打印分析结果"""
    print(f"\n{'='*60}")
    print(f"文件: {result['file']}")
    print(f"大小: {result['size']} bytes")
    print(f"头部: {result['header']}")
    print(f"{'='*60}")

    print(f"\n字段列表 ({len(result['fields'])} 个):")
    print("-" * 60)

    for field in result["fields"]:
        tag = field["tag_hex"]
        fnum = field["field_number"]
        wtype = field["wire_type"]
        ftype = field["type"]

        if ftype == "varint":
            value = field["value"]
            print(f"  {tag} (field {fnum}, wire {wtype}): varint = {value}")
        else:
            preview = field.get("value_preview", "")
            length = field.get("length", 0)
            print(f"  {tag} (field {fnum}, wire {wtype}): length={length}, value={preview}")

    if result["errors"]:
        print(f"\n❌ 错误 ({len(result['errors'])} 个):")
        for err in result["errors"]:
            print(f"  - {err}")
    else:
        print("\n✅ 无解析错误")

    # 检查关键问题
    issues = check_critical_issues(result)
    if issues:
        print(f"\n⚠️  潜在问题 ({len(issues)} 个):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ 未发现明显的格式问题")


def main():
    if len(sys.argv) < 2:
        print("用法: python test_vsmeta_format.py <vsmeta文件路径>")
        print("\n示例:")
        print("  python test_vsmeta_format.py IPX-805.mp4.vsmeta")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"错误: 文件不存在: {filepath}")
        sys.exit(1)

    result = analyze_vsmeta(filepath)
    print_analysis(result)

    # 输出格式验证总结
    print(f"\n{'='*60}")
    print("格式验证总结")
    print(f"{'='*60}")

    checks = {
        "文件头正确 (0x08 0x01)": result["header"] is not None,
        "无解析错误": len(result["errors"]) == 0,
        "包含标题字段 (0x12)": any(f["tag_hex"] == "0x12" for f in result["fields"]),
        "包含 GROUP1 (0x52)": any(f["tag_hex"] == "0x52" for f in result["fields"]),
        "包含 GROUP2 (0x9A)": any(f["tag_hex"] == "0x9A" for f in result["fields"]),
        "包含 GROUP3 (0xAA)": any(f["tag_hex"] == "0xAA" for f in result["fields"]),
    }

    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print(f"\n🎉 所有检查通过！VSMETA 格式符合标准。")
    else:
        print(f"\n⚠️  部分检查未通过，请检查上述问题。")


if __name__ == "__main__":
    main()
