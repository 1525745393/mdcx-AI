#!/usr/bin/env python3
"""特别检查 VSMETA 文件的索引字节"""

import sys
from pathlib import Path

def check_index_bytes(filepath):
    """检查索引字节"""
    data = Path(filepath).read_bytes()
    print(f"检查文件: {filepath}")
    
    offset = 0
    
    # 跳过头部
    if offset + 2 <= len(data) and data[offset:offset+2] == b'\x08\x01':
        offset += 2
    
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
            
            # 特别检查重要的标签
            if tag_byte in [0x8A, 0x92, 0x9A, 0xAA]:
                print(f"\n标签 0x{tag_byte:02x} (field {field_num})")
                print(f"  偏移: 0x{offset - 1:x}")
                
                # 检查是否有索引字节
                if offset < len(data) and data[offset] == 0x01:
                    print(f"  ✅ 检测到索引字节 0x01 在偏移 0x{offset:x}")
                    
                    # 检查索引字节后的 varint 长度
                    actual_length, actual_off = decode_varint(data, offset + 1)
                    print(f"  索引字节后的真实长度: {actual_length}")
                else:
                    print(f"  ❌ 未找到索引字节 0x01")
                
                # 打印前几个字节
                preview_len = min(20, len(data) - offset)
                preview = data[offset:offset + preview_len]
                print(f"  标签后前 {preview_len} 字节: {' '.join(f'{b:02x}' for b in preview)}")
            
            offset += length
        elif wire_type == 0:
            val, offset = decode_varint(data, offset)

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
    print("=" * 70)
    print("检查 IPX-967.mp4.vsmeta 的索引字节")
    print("=" * 70)
    check_index_bytes("IPX-967.mp4.vsmeta")
    
    print("\n" + "=" * 70)
    print("检查 IPX-805.mp4.vsmeta 的索引字节")
    print("=" * 70)
    check_index_bytes("IPX-805.mp4.vsmeta")
