#!/usr/bin/env python3
"""简洁版分析脚本，重点查找重要字段的位置"""

import sys
from pathlib import Path


def find_important_tags(filepath):
    """只查找重要的标签"""
    data = Path(filepath).read_bytes()
    
    print(f"{'='*70}")
    print(f"分析文件: {filepath}")
    print(f"{'='*70}")
    print(f"大小: {len(data)} 字节")
    print()
    
    important_tags = {
        0x8A: "TAG_EPISODE_THUMB_DATA",
        0x92: "TAG_EPISODE_THUMB_MD5",
        0x9A: "TAG_GROUP2",
        0xAA: "TAG_GROUP3",
    }
    
    offset = 0
    # 检查头部
    if offset + 2 <= len(data) and data[offset:offset+2] == b'\x08\x01':
        offset += 2
    
    found = {}
    
    while offset < len(data):
        if offset + 1 > len(data):
            break
        
        tag_byte = data[offset]
        offset += 1
        
        field_num = tag_byte >> 3
        wire_type = tag_byte & 0x07
        
        if wire_type == 2:  # Length-delimited
            length, new_off = decode_varint(data, offset)
            offset = new_off
            
            if tag_byte in important_tags:
                name = important_tags[tag_byte]
                print(f"✓ 找到 {name} (0x{tag_byte:02x}) 在偏移 0x{offset - 1:x}")
                
                # 检查索引字节
                has_index = False
                if offset < len(data) and data[offset] == 0x01:
                    has_index = True
                    print(f"    ✅ 有索引字节 0x01 在偏移 0x{offset:x}")
                    # 检查索引后的长度
                    if offset + 1 < len(data):
                        actual_len, _ = decode_varint(data, offset + 1)
                        print(f"    索引后长度: {actual_len}")
                else:
                    print(f"    ❌ 没有索引字节")
                
                # 检查图片
                if offset + 2 < len(data):
                    if data[offset:offset+2] == b'\xff\xd8':
                        print(f"    🖼️ 原始 JPEG 图片")
                    elif offset + 4 < len(data) and data[offset:offset+4] == b'/9j/':
                        print(f"    📝 Base64 编码的图片")
                
                # 打印前10字节
                preview_len = min(15, len(data) - offset)
                preview = data[offset:offset + preview_len]
                print(f"    字段后前 {preview_len} 字节: {' '.join(f'{b:02x}' for b in preview)}")
                
                print()
                found[name] = (has_index, data[offset:offset+2])
            
            offset += length
        elif wire_type == 0:
            val, offset = decode_varint(data, offset)
    
    return found


def decode_varint(data, offset):
    """解码 varint"""
    result = 0
    shift = 0
    while offset < len(data):
        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1
        if not (byte & 0x80):
            break
        shift += 7
    return result, offset


if __name__ == "__main__":
    # 对比分析所有文件
    files = [
        "MIDE-599.mp4.vsmeta",
        "IPX-967.mp4.vsmeta",
        "IPX-805.mp4.vsmeta",
        "test_fixed.vsmeta",
    ]
    
    all_results = {}
    
    for f in files:
        try:
            all_results[f] = find_important_tags(f)
        except Exception as e:
            print(f"❌ 分析 {f} 失败: {e}")
            print()
    
    # 总结对比
    print(f"{'='*70}")
    print(f"对比总结")
    print(f"{'='*70}")
    
    print("{:<30} {:<15} {:<15}".format("文件", "索引字节", "图片格式"))
    print("-" * 60)
    
    for filename, results in all_results.items():
        has_index = "✅" if results.get("TAG_GROUP2", (False, None))[0] else "❌"
        
        # 检查图片格式
        img_format = "?"
        if "TAG_EPISODE_THUMB_DATA" in results:
            _, data = results["TAG_EPISODE_THUMB_DATA"]
            if data == b'\xff\xd8':
                img_format = "原始JPEG"
            elif len(data) >= 4 and data[:4] == b'/9j/':
                img_format = "Base64"
        
        print("{:<30} {:<15} {:<15}".format(filename, has_index, img_format))
