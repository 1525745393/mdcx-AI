#!/usr/bin/env python3

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

def find_all_markers(filename, marker):
    positions = []
    with open(filename, 'rb') as f:
        data = f.read()
    pos = 0
    while True:
        pos = data.find(marker, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos +=1
    return positions

print("=== File1 (good) 0xaa positions: ===")
aa_pos1 = find_all_markers(file1, b'\xaa')
for pos in aa_pos1:
    print(f"  0x{pos:06x}")

print("\n=== File2 (bad) 0xaa positions: ===")
aa_pos2 = find_all_markers(file2, b'\xaa')
for pos in aa_pos2:
    print(f"  0x{pos:06x}")


# Now let's check the 0xaa tag that should be GROUP3!
# 让我们找到两个文件中在 0x247af 之后第一个 0xaa
def read_at_offset(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        return f.read(length)

print("\n=== Checking first 0xaa after GROUP2 in File1: ===")
for pos in aa_pos1:
    if pos > 0x24700:
        print(f"\n0xaa found at 0x{pos:06x}")
        data = read_at_offset(file1, pos, 200)
        for i in range(0, len(data), 16):
            off = pos + i
            chunk = data[i:i+16]
            print(f"0x{off:06x} | {chunk.hex()} | {''.join(chr(c) if 32<=c<127 else '.' for c in chunk)}")
        break

print("\n=== Checking first 0xaa after GROUP2 in File2: ===")
for pos in aa_pos2:
    if pos > 0x24700:
        print(f"\n0xaa found at 0x{pos:06x}")
        data = read_at_offset(file2, pos, 200)
        for i in range(0, len(data), 16):
            off = pos + i
            chunk = data[i:i+16]
            print(f"0x{off:06x} | {chunk.hex()} | {''.join(chr(c) if 32<=c<127 else '.' for c in chunk)}")
        break
