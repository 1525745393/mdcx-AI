#!/usr/bin/env python3

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

def read_at_offset(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        return f.read(length)

# 读取 GROUP2 内容：tag(1) + index(1) + len_varint(3) + content(47)
# File1: content starts at 0x2477d +3 =0x24780
# File2: content starts at 0x247c2 +3 =0x247c5
g2_content1 = read_at_offset(file1, 0x24780, 47)
g2_content2 = read_at_offset(file2, 0x247c5, 47)

print("=== GROUP2 Content File1 (good): ===")
print(f"  Hex: {g2_content1.hex()}")
try:
    print(f"  ASCII: {g2_content1.decode('utf-8', errors='replace')}")
except Exception as e:
    print(f"  Decode error: {e}")

print("\n=== GROUP2 Content File2 (bad): ===")
print(f"  Hex: {g2_content2.hex()}")
try:
    print(f"  ASCII: {g2_content2.decode('utf-8', errors='replace')}")
except Exception as e:
    print(f"  Decode error: {e}")

print("\n=== Difference: ===")
if g2_content1 == g2_content2:
    print("GROUP2 content is identical!")
else:
    print("GROUP2 content differs!")
    for i, (b1, b2) in enumerate(zip(g2_content1, g2_content2)):
        if b1 != b2:
            print(f"  Byte {i}: File1=0x{b1:02x}, File2=0x{b2:02x}")


print("\n=== Now let's look at what comes after GROUP2 (GROUP3 and pictures)! ===")

# 查找 GROUP3 位置！
data1_full = read_at_offset(file1, 0, 0x250000)
data2_full = read_at_offset(file2, 0, 0x250000)

# Find 0xaa (GROUP3 tag) after GROUP2
pos_after_g2_1 = 0x24780 +47
pos_after_g2_2 = 0x247c5 +47

print(f"\nFile1 after GROUP2 (pos 0x{pos_after_g2_1:x}):")
chunk1 = data1_full[pos_after_g2_1 : pos_after_g2_1 + 200]
for i in range(0, len(chunk1), 16):
    off = pos_after_g2_1 + i
    c = chunk1[i:i+16]
    print(f"0x{off:06x} | {c.hex()} | {''.join(chr(x) if 32<=x<127 else '.' for x in c)}")

print(f"\nFile2 after GROUP2 (pos 0x{pos_after_g2_2:x}):")
chunk2 = data2_full[pos_after_g2_2 : pos_after_g2_2 + 200]
for i in range(0, len(chunk2), 16):
    off = pos_after_g2_2 + i
    c = chunk2[i:i+16]
    print(f"0x{off:06x} | {c.hex()} | {''.join(chr(x) if 32<=x<127 else '.' for x in c)}")
