#!/usr/bin/env python3
"""直接查看文件开头的详细结构"""

from pathlib import Path


def print_hex_dump(data, label, max_len=200):
    """打印十六进制和ASCII"""
    print(f"\n{'='*70}")
    print(f"{label} (前 {min(max_len, len(data))} 字节)")
    print(f"{'='*70}")
    
    print("   00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
    print(" " + "-" * 49)
    
    for i in range(0, min(max_len, len(data)), 16):
        line = data[i:i+16]
        hex_str = " ".join(f"{b:02x}" for b in line)
        ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in line)
        print(f"{i:04x} {hex_str:<47} {ascii_str}")


def analyze_file_structure(filepath, label):
    """简单分析文件结构"""
    data = Path(filepath).read_bytes()
    print_hex_dump(data, label, 300)
    
    # 检查头部
    print("\n头部检查:")
    if len(data) >= 2 and data[:2] == b'\x08\x01':
        print("  ✓ Movie (0x08 0x01)")
    else:
        print(f"  ✗ 未知头部: {data[:2].hex()}")


if __name__ == "__main__":
    # 先分析 MIDE-599.mp4.vsmeta
    analyze_file_structure("MIDE-599.mp4.vsmeta", "MIDE-599.mp4.vsmeta - 可识别的文件")
    
    # 再对比我们的测试文件
    print("\n"*2)
    analyze_file_structure("test_fixed.vsmeta", "test_fixed.vsmeta - 我们的测试文件")
    
    # 再看 IPX-967.mp4.vsmeta
    print("\n"*2)
    analyze_file_structure("IPX-967.mp4.vsmeta", "IPX-967.mp4.vsmeta")
