#!/usr/bin/env python3

def find_all_markers(filename, marker):
    results = []
    with open(filename, 'rb') as f:
        data = f.read()
        pos = 0
        while True:
            pos = data.find(marker, pos)
            if pos == -1:
                break
            results.append(pos)
            pos += 1
    return results

file1 = '/workspace/IPX-967.mp4.vsmeta'
file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'

# Find JPEG start (FF D8 FF)
jpeg_marker = b'\xff\xd8\xff'
pos1_jpeg = find_all_markers(file1, jpeg_marker)
pos2_jpeg = find_all_markers(file2, jpeg_marker)

print('='*70)
print(f'File1 (good): {file1}')
print(f'  Size: {open(file1, "rb").seek(0,2)} bytes')
print(f'  JPEG starts at: {[f"0x{x:06x}" for x in pos1_jpeg]}')
print()
print(f'File2 (bad): {file2}')
print(f'  Size: {open(file2, "rb").seek(0,2)} bytes')
print(f'  JPEG starts at: {[f"0x{x:06x}" for x in pos2_jpeg]}')
print()

# 现在对比两个文件中 290000-300000 这个区域（GROUP2 和 GROUP3 附近）
def compare_region(f1, f2, start, end):
    print(f'\nComparing {f1} vs {f2} from 0x{start:x} to 0x{end:x}:')
    d1 = open(f1, 'rb').read()[start:end]
    d2 = open(f2, 'rb').read()[start:end]
    if d1 == d2:
        print('  Same!')
    else:
        print('  Different!')
        # Find the first differing position
        for i, (b1, b2) in enumerate(zip(d1, d2)):
            if b1 != b2:
                print(f'  First different at 0x{start+i:x}: 0x{b1:02x} vs 0x{b2:02x}')
                break

# 查找 GROUP2 和 GROUP3 以及 JPEG
print("\n--- Checking positions around 290000 to 310000 ---")
with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
    f1.seek(297000)
    f2.seek(297000)
    d1 = f1.read(1000)
    d2 = f2.read(1000)
    print(f"File1 at 297000: {d1[:80].hex()}")
    print(f"File2 at 297000: {d2[:80].hex()}")
    
    # Find 0x9a (GROUP2 tag) and 0xaa (GROUP3 tag)
    def find_tag(data, tag):
        pos = []
        for i in range(len(data)-1):
            if data[i] == tag:
                pos.append(i)
        return pos
    
    print(f"\nFile1 has tags at 297000+:")
    print(f"  0x9a (GROUP2): {[297000 + x for x in find_tag(d1, 0x9a)[:5]]}")
    print(f"  0xaa (GROUP3): {[297000 + x for x in find_tag(d1, 0xaa)[:5]]}")
    
    print(f"\nFile2 has tags at 297000+:")
    print(f"  0x9a (GROUP2): {[297000 + x for x in find_tag(d2, 0x9a)[:5]]}")
    print(f"  0xaa (GROUP3): {[297000 + x for x in find_tag(d2, 0xaa)[:5]]}")
