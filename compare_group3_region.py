#!/usr/bin/env python3

def read_at_offset(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        return f.read(length)

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

# 读取 GROUP3 附近
# File1 GROUP3 at 297645 → start 297600 for context
data1 = read_at_offset(file1, 297550, 200)
# File2 GROUP3 at 297714 → start 297620
data2 = read_at_offset(file2, 297620, 200)

print('='*80)
print(f'File1 (good) around 297645 (GROUP3 at 297645):')
print('='*80)

def print_hex_with_offset(data, base):
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        mark = ' <--' if (base + i == 297645) else ''
        print(f'0x{base+i:06x} | {hex_str:<48} | {ascii_str:<16}{mark}')

print_hex_with_offset(data1, 297550)

print()
print('='*80)
print(f'File2 (bad) around 297714 (GROUP3 at 297714):')
print('='*80)
print_hex_with_offset(data2, 297620)

print()
print('='*80)
print('Now checking what comes right after GROUP3 (the poster and MD5):')
print('='*80)

# 现在直接用 vsmeta 生成逻辑，找到差异！让我们查看 vsmeta 的实际编码逻辑，特别是
# 当写入 GROUP2, GROUP3 时的差异！让我们直接查看这两个文件之间从 EPISODE_THUMB_MD5 之后的偏移差异！
print("\n--- Finding where exactly the 69-byte difference happens ---")
# 让我们逐字节对比直到找到第一个不同点
with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
    d1 = f1.read()
    d2 = f2.read()
    
    min_len = min(len(d1), len(d2))
    diff_pos = -1
    for i in range(min_len):
        if d1[i] != d2[i]:
            diff_pos = i
            print(f"First difference at offset 0x{i:06x}")
            print(f"File1: 0x{d1[i]:02x}")
            print(f"File2: 0x{d2[i]:02x}")
            
            # 打印差异位置前后的 200 字节
            print("\n--- File1 around 0x%06x:" % (diff_pos))
            start = max(0, diff_pos - 100)
            end = min(len(d1), diff_pos + 100)
            print('  ' + d1[start:end].hex())
            print("\n--- File2 around 0x%06x:" % (diff_pos))
            start2 = max(0, diff_pos - 100)
            end2 = min(len(d2), diff_pos + 100)
            print('  ' + d2[start2:end2].hex())
            break
    else:
        print("All bytes are the same up to length of shorter file.")
