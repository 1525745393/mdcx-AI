#!/usr/bin/env python3

def hexdump_region(filename: str, start: int, end: int):
    with open(filename, 'rb') as f:
        data = f.read()
    print(f"\n--- {filename} 0x{start:06x} to 0x{end:06x} ---")
    for i in range(start, min(end, len(data)), 16):
        chunk = data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
        print(f"0x{i:06x}  {hex_str:<48} |{ascii_str}|")

hexdump_region("/workspace/IPX-967.mp4.vsmeta", 0x400, 0x550)
hexdump_region("/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta", 0x400, 0x550)
