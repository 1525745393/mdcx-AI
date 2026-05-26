#!/usr/bin/env python3

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

# 查找两个文件中的相同的 32 字节的十六进制字符串（可能是 MD5）
with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
    data1 = f1.read()
    data2 = f2.read()
    
    # 查找 common sequences of length 32-100 bytes
    # 我们知道这两个文件应该有相同的图片数据，所以找一个长的共同子串！
    min_len = 500
    print(f"Looking for common substring of length >= {min_len}...")
    for i in range(len(data1) - min_len):
        substr = data1[i:i+min_len]
        pos2 = data2.find(substr)
        if pos2 != -1:
            print(f"Found common substring starting at File1: 0x{i:06x}, File2: 0x{pos2:06x}")
            print(f"Length of common prefix at this point: {i} vs {pos2}, difference: {pos2 - i}")
            break
    else:
        print("No common substring found")

# 查找 MD5 字符串：32 个十六进制字符
print("\nLooking for 32-byte hex sequences (possible MD5):")
def find_all_hex_strings(data):
    hex_chars = b'0123456789abcdefABCDEF'
    results = []
    pos = 0
    while pos < len(data) - 32:
        # 查找连续的32个十六进制字符
        valid = True
        for i in range(32):
            if data[pos+i] not in hex_chars:
                valid = False
                break
        if valid:
            results.append((pos, data[pos:pos+32]))
        pos += 1
    return results

hex1 = find_all_hex_strings(data1)
hex2 = find_all_hex_strings(data2)

print(f"\nFile1 found {len(hex1)} hex sequences")
print(f"File2 found {len(hex2)} hex sequences")

print("\nLooking for common hex sequences:")
common_md5 = None
for pos1, md5_1 in hex1:
    for pos2, md5_2 in hex2:
        if md5_1 == md5_2:
            print(f"  Found MD5: {md5_1.decode('ascii')} at File1:0x{pos1:x}, File2:0x{pos2:x}")
            common_md5 = (pos1, pos2, md5_1)
            break
    if common_md5:
        break

if common_md5:
    pos1, pos2, md5 = common_md5
    print(f"\n--- Now comparing area around MD5 in both files ---")
    
    # 读取 MD5 前面的区域，查看 TAG 结构！
    # vsmeta.py 中 EPISODE_THUMB_MD5 是带索引字节的 0x92 01 <length> <md5_str>
    print("\nFile1 around MD5 (0x%x):" % pos1)
    start1 = max(0, pos1 - 50)
    end1 = min(len(data1), pos1 + 50)
    chunk1 = data1[start1:end1]
    for i in range(0, len(chunk1), 16):
        offset = start1 + i
        line_data = chunk1[i:i+16]
        hex_line = ' '.join(f'{b:02x}' for b in line_data)
        ascii_line = ''.join(chr(b) if 32<=b<127 else '.' for b in line_data)
        mark = ' <-- MD5' if (offset <= pos1 < offset+16) else ''
        print(f"0x{offset:06x} | {hex_line:<48} | {ascii_line:<16} {mark}")

    print("\nFile2 around MD5 (0x%x):" % pos2)
    start2 = max(0, pos2 - 50)
    end2 = min(len(data2), pos2 + 50)
    chunk2 = data2[start2:end2]
    for i in range(0, len(chunk2), 16):
        offset = start2 + i
        line_data = chunk2[i:i+16]
        hex_line = ' '.join(f'{b:02x}' for b in line_data)
        ascii_line = ''.join(chr(b) if 32<=b<127 else '.' for b in line_data)
        mark = ' <-- MD5' if (offset <= pos2 < offset+16) else ''
        print(f"0x{offset:06x} | {hex_line:<48} | {ascii_line:<16} {mark}")
