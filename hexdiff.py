#!/usr/bin/env python3


def read_hex(file_path, offset=0, length=2000):
    """Read file as hex dump"""
    with open(file_path, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
    return data


def print_hex_diff(data1, data2, label1="File1", label2="File2"):
    """Print hex comparison of two data blocks"""
    print(f"\n{'='*80}")
    print(f"Comparing {label1} vs {label2}")
    print(f"{'='*80}")
    
    offset = 0
    chunk_size = 16
    
    while offset < max(len(data1), len(data2)):
        chunk1 = data1[offset:offset+chunk_size] if offset < len(data1) else b''
        chunk2 = data2[offset:offset+chunk_size] if offset < len(data2) else b''
        
        hex1 = ' '.join(f'{b:02x}' for b in chunk1).ljust(48)
        hex2 = ' '.join(f'{b:02x}' for b in chunk2).ljust(48)
        
        # Try to decode as ASCII
        ascii1 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk1)
        ascii2 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk2)
        
        has_diff = chunk1 != chunk2
        marker = '*' if has_diff else ' '
        
        print(f"{marker} {offset:06x} | {hex1} | {ascii1:<16} | {hex2} | {ascii2:<16}")
        
        offset += chunk_size


if __name__ == '__main__':
    file1 = '/workspace/IPX-967.mp4.vsmeta'
    file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'
    
    data1 = read_hex(file1, length=3000)
    data2 = read_hex(file2, length=3000)
    
    print_hex_diff(data1, data2, "Good", "Bad")
