#!/usr/bin/env python3
"""详细分析 VSMETA 文件，重点检查索引字节"""

import sys
from pathlib import Path

def analyze_vsmeta_detailed(filepath):
    """详细分析 VSMETA 文件，特别关注索引字节"""
    data = Path(filepath).read_bytes()
    print(f"文件: {filepath}")
    print(f"大小: {len(data)} 字节")
    print(f"\n前50字节 (头部): {' '.join(f'{b:02x}' for b in data[:50])}")
    
    offset = 0
    
    # 检查头部
    if offset + 2 <= len(data) and data[offset:offset+2] == b'\x08\x01':
        print(f"头部: ✅ Movie (0x08 0x01)")
        offset += 2
    else:
        print(f"头部: ❌ 无效")
        return
    
    print(f"\n--- 字段详细分析 ---")
    
    while offset < len(data):
        if offset + 1 > len(data):
            break
        
        tag_byte = data[offset]
        field_num = tag_byte >> 3
        wire_type = tag_byte & 0x07
        offset += 1
        
        print(f"\n偏移 {offset-1:06x}, 标签 {tag_byte:02x} (field {field_num}, wire {wire_type})")
        
        if wire_type == 0:  # Varint
            val, new_off = decode_varint(data, offset)
            print(f"  Varint: {val}")
            offset = new_off
        elif wire_type == 2:  # Length-delimited
            length, new_off = decode_varint(data, offset)
            offset = new_off
            
            # 检查是否有索引字节
            has_index_byte = False
            if offset < len(data):
                if data[offset] == 0x01:
                    has_index_byte = True
                    print(f"  ⚠️ 检测到索引字节 0x01！")
                    # 跳过索引字节，检查实际长度
                    actual_length, new_off2 = decode_varint(data, offset + 1)
                    print(f"  索引字节后的长度: {actual_length}")
                    offset += 1
            
            print(f"  长度: {length}")
            
            if length > 0 and offset + length <= len(data):
                payload = data[offset:offset+length]
                # 检查是否是 Base64
                if payload.startswith(b'/9j/'):
                    print(f"  内容: ⚠️ Base64 编码的图片")
                elif len(payload) < 100:
                    try:
                        print(f"  内容: {payload.decode('utf-8', errors='replace')}")
                    except:
                        print(f"  内容: 二进制, 前20字节: {' '.join(f'{b:02x}' for b in payload[:20])}")
                else:
                    print(f"  内容: 二进制, 前20字节: {' '.join(f'{b:02x}' for b in payload[:20])}")
            
            offset += length

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
    print("详细分析 IPX-967.mp4.vsmeta")
    print("=" * 70)
    analyze_vsmeta_detailed("IPX-967.mp4.vsmeta")
    
    print("\n" + "=" * 70)
    print("详细分析 IPX-805.mp4.vsmeta")
    print("=" * 70)
    analyze_vsmeta_detailed("IPX-805.mp4.vsmeta")
