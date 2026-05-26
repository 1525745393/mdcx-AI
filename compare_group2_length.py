#!/usr/bin/env python3

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

# 已知 MD5 位置：File1:0x2475b, File2:0x247a0
# MD5 长度是 32 字节，所以 MD5 结束在 File1:0x2475b+32 =0x2477b, File2:0x247a0+32=0x247c0
def read_at_offset(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        return f.read(length)

print("=== File1 (good) from MD5 end (0x2477b): ===")
data1 = read_at_offset(file1, 0x24760, 100)
for i in range(0, len(data1), 16):
    off = 0x24760 + i
    chunk = data1[i:i+16]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    asc_str = ''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
    mark = ' <-- GROUP2' if (off == 0x2477b) else ''
    print(f'0x{off:06x} | {hex_str:<48} | {asc_str} {mark}')

print("\n=== File2 (bad) from MD5 end (0x247c0): ===")
data2 = read_at_offset(file2, 0x247a0, 100)
for i in range(0, len(data2), 16):
    off = 0x247a0 + i
    chunk = data2[i:i+16]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    asc_str = ''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
    mark = ' <-- GROUP2' if (off == 0x247c0) else ''
    print(f'0x{off:06x} | {hex_str:<48} | {asc_str} {mark}')


print("\n--- Now let's decode the varints for GROUP2 in both files! ---")

def decode_varint_at(data, offset):
    result = 0
    shift = 0
    i = 0
    while True:
        byte = data[offset+i]
        result |= (byte & 0x7F) << shift
        i +=1
        if not (byte & 0x80):
            break
    return result, i

# File1: from 0x2477b
d1_group2_start = 0x2477b
group2_data1 = read_at_offset(file1, d1_group2_start, 20)
print("File1 GROUP2 area:")
print(f"  0x{d1_group2_start:06x}: tag is 0x{group2_data1[0]:02x}")
print(f"  0x{d1_group2_start+1:06x}: index is 0x{group2_data1[1]:02x}")
len_val1, len_bytes1 = decode_varint_at(group2_data1, 2)
print(f"  0x{d1_group2_start+2:06x}: varint length: {len_val1} (uses {len_bytes1} bytes)")

d2_group2_start = 0x247c0
group2_data2 = read_at_offset(file2, d2_group2_start, 20)
print("\nFile2 GROUP2 area:")
print(f"  0x{d2_group2_start:06x}: tag is 0x{group2_data2[0]:02x}")
print(f"  0x{d2_group2_start+1:06x}: index is 0x{group2_data2[1]:02x}")
len_val2, len_bytes2 = decode_varint_at(group2_data2, 2)
print(f"  0x{d2_group2_start+2:06x}: varint length: {len_val2} (uses {len_bytes2} bytes)")
