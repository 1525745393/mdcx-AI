#!/usr/bin/env python3
"""深入对比分析 MIDE-599.mp4.vsmeta 的完整结构"""

import sys
from pathlib import Path


def analyze_field_details(filepath, tag_name, tag_val):
    """分析特定字段的详细信息"""
    data = Path(filepath).read_bytes()
    offset = 0
    
    # 跳过头部
    if offset + 2 <= len(data) and data[offset:offset+2] == b'\x08\x01':
        offset += 2
    
    while offset < len(data):
        if offset + 1 > len(data):
            break
        
        tag_byte = data[offset]
        offset += 1
        
        if tag_byte == tag_val:
            print(f"\n{'='*60}")
            print(f"字段分析: {tag_name} (0x{tag_val:02x})")
            print(f"{'='*60}")
            print(f"字段起始偏移: 0x{offset - 1:x}")
            
            wire_type = tag_byte & 0x07
            if wire_type == 2:
                length, offset = decode_varint(data, offset)
                print(f"wire type: 2 (长度前缀)")
                print(f"声明长度: {length} 字节")
                print(f"实际内容偏移: 0x{offset:x}")
                
                # 打印内容的前100字节
                preview_len = min(100, length)
                preview = data[offset:offset + preview_len]
                
                print("\n前100字节内容:")
                print(f"   00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
                print(" " + "-" * 49)
                
                for i in range(0, preview_len, 16):
                    line = preview[i:i+16]
                    hex_str = " ".join(f"{b:02x}" for b in line)
                    ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in line)
                    print(f"{i:04x} {hex_str:<47} {ascii_str}")
                
                # 检查是否是 JPEG
                if length >= 2 and data[offset:offset+2] == b'\xff\xd8':
                    print("\n✓ 这是原始 JPEG 图片!")
                    return True
                # 检查 Base64
                elif length >= 4 and data[offset:offset+4] == b'/9j/':
                    print("\n✓ 这是 Base64 编码的图片!")
                    return True
                else:
                    print("\n? 未知格式")
                    
                return True
            
            break
        
        # 继续下一个字段
        wire_type = tag_byte & 0x07
        if wire_type == 0:
            _, offset = decode_varint(data, offset)
        elif wire_type == 2:
            _, offset = decode_varint(data, offset)
            length, _ = decode_varint(data, offset)
            offset += length
    
    return False


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
    print(f"{'='*70}")
    print(f"深入分析 MIDE-599.mp4.vsmeta")
    print(f"{'='*70}")
    
    # 分析重要字段
    analyze_field_details("MIDE-599.mp4.vsmeta", "TAG_EPISODE_THUMB_DATA", 0x8a)
    analyze_field_details("MIDE-599.mp4.vsmeta", "TAG_GROUP2", 0x9a)
    
    # 对比我们生成的文件
    print(f"\n{'='*70}")
    print(f"对比我们生成的 test_fixed.vsmeta")
    print(f"{'='*70}")
    analyze_field_details("test_fixed.vsmeta", "TAG_EPISODE_THUMB_DATA", 0x8a)
