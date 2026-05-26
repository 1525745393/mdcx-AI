#!/usr/bin/env python3
"""专门对比分析 MIDE-599.mp4.vsmeta 这个正确的文件"""

import sys
from pathlib import Path


def analyze_correct_file(filepath):
    """详细分析正确的文件"""
    data = Path(filepath).read_bytes()
    print(f"{'='*70}")
    print(f"分析文件: {filepath}")
    print(f"{'='*70}")
    print(f"大小: {len(data)} 字节")
    
    offset = 0
    
    # 检查头部
    if offset + 2 <= len(data) and data[offset:offset+2] == b'\x08\x01':
        print(f"✅ 头部: Movie (0x08 0x01)")
        offset += 2
    else:
        print(f"❌ 无效头部")
        return
    
    print(f"\n{'='*70}")
    print("字段详细分析")
    print(f"{'='*70}")
    
    tags_found = []
    
    while offset < len(data):
        if offset + 1 > len(data):
            break
        
        tag_byte = data[offset]
        field_num = tag_byte >> 3
        wire_type = tag_byte & 0x07
        tag_info = f"0x{tag_byte:02x} (field {field_num}, wire {wire_type})"
        offset += 1
        
        print(f"\n偏移 {offset-1:06x} - {tag_info}")
        
        if wire_type == 0:  # Varint
            val, new_off = decode_varint(data, offset)
            print(f"  Varint: {val}")
            offset = new_off
        elif wire_type == 2:  # Length-delimited
            length, new_off = decode_varint(data, offset)
            offset = new_off
            
            # 检查是否是组字段
            if tag_byte in [0x8A, 0x92, 0x9A, 0xAA]:
                print(f"  ⚠️  重要字段！")
            
            # 打印标签和长度后的几个字节
            preview_len = min(30, len(data) - offset)
            preview = data[offset:offset + preview_len]
            print(f"  长度: {length}")
            print(f"  标签后前 {preview_len} 字节: {' '.join(f'{b:02x}' for b in preview)}")
            
            # 检查 payload 的开头
            if length > 0 and offset < len(data):
                first_byte = data[offset]
                if first_byte == 0x01:
                    print(f"  ✅ 有索引字节 0x01!")
                
                # 检查 JPEG
                if offset + 2 < len(data) and data[offset:offset+2] == b'\xff\xd8':
                    print(f"  🖼️ 这是原始 JPEG 图片")
                elif offset + 4 < len(data) and data[offset:offset+4] == b'/9j/':
                    print(f"  📝 这是 Base64 编码的图片")
                
                # 短字符串
                if length < 200 and length > 0:
                    try:
                        substr = data[offset:offset + min(100, length)].decode('utf-8', errors='replace')
                        print(f"  内容: {repr(substr)}")
                    except:
                        pass
            
            tags_found.append((tag_byte, offset-1, length))
            offset += length
    
    return tags_found


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
    # 只分析 MIDE-599.mp4.vsmeta
    if len(sys.argv) > 1:
        file_to_analyze = sys.argv[1]
    else:
        file_to_analyze = "MIDE-599.mp4.vsmeta"
    
    tags_found = analyze_correct_file(file_to_analyze)
    
    print(f"\n{'='*70}")
    print("分析完成！总结:")
    print(f"{'='*70}")
    
    # 总结重要标签
    important_tags = {
        0x8A: "TAG_EPISODE_THUMB_DATA",
        0x92: "TAG_EPISODE_THUMB_MD5",
        0x9A: "TAG_GROUP2",
        0xAA: "TAG_GROUP3",
    }
    
    for tag, offset, length in tags_found:
        if tag in important_tags:
            print(f"  {important_tags[tag]} (0x{tag:02x}) 在偏移 0x{offset:x}")
