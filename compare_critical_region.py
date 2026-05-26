#!/usr/bin/env python3

def read_range(filename, start, end):
    with open(filename, 'rb') as f:
        f.seek(start)
        return f.read(end - start)

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

# 从 GROUP1 结束附近开始对比
data1 = read_range(file1, 0x0490, 0x0580) 
data2 = read_range(file2, 0x04d0, 0x05c0)

print('=' * 80)
print(f'File1: {file1} offset 0x0490-0x0580')
print(f'File2: {file2} offset 0x04d0-0x05c0')
print('=' * 80)
print()

def print_hex(data, offset_base, label):
    print(f'{label}:')
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b <127 else '.' for b in chunk)
        print(f'  0x{offset_base + i:04x} | {hex_str:<48} | {ascii_str}')
    print()

print_hex(data1, 0x0490, 'File1 (good)')
print_hex(data2, 0x04d0, 'File2 (bad)')
