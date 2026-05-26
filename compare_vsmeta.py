#!/usr/bin/env python3
import os

def compare_files(file1_path, file2_path):
    with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"文件1大小: {len(data1)} 字节")
    print(f"文件2大小: {len(data2)} 字节")
    print()
    
    if data1 == data2:
        print("两个文件完全相同！")
        return
    
    print("文件内容不同！")
    print()
    
    # 找出不同位置
    min_len = min(len(data1), len(data2))
    diff_positions = []
    for i in range(min_len):
        if data1[i] != data2[i]:
            diff_positions.append(i)
            if len(diff_positions) > 100:  # 只显示前100个差异位置
                break
    
    print(f"前 {len(diff_positions)} 个差异位置:")
    for pos in diff_positions[:20]:  # 只显示前20个
        byte1 = data1[pos]
        byte2 = data2[pos]
        print(f"  位置 {pos}: 0x{byte1:02x} vs 0x{byte2:02x}")
    
    if len(diff_positions) >= 100:
        print("  ... 还有更多差异")
    
    print()
    
    # 尝试提取可打印的文本内容
    def extract_text(data):
        text = []
        current = []
        for byte in data:
            if 32 <= byte <= 126 or byte in (9, 10, 13):
                current.append(chr(byte))
            else:
                if current:
                    text.append(''.join(current))
                    current = []
        if current:
            text.append(''.join(current))
        return [t for t in text if len(t.strip()) > 1]
    
    text1 = extract_text(data1)
    text2 = extract_text(data2)
    
    print("=" * 60)
    print("文件1中的文本内容:")
    print("=" * 60)
    for i, t in enumerate(text1[:30]):  # 显示前30段
        print(f"[{i}] {repr(t)}")
    
    print()
    print("=" * 60)
    print("文件2中的文本内容:")
    print("=" * 60)
    for i, t in enumerate(text2[:30]):  # 显示前30段
        print(f"[{i}] {repr(t)}")
    
    print()
    print("=" * 60)
    print("文件开头100字节的十六进制比较:")
    print("=" * 60)
    print("文件1:")
    print(' '.join(f'{b:02x}' for b in data1[:100]))
    print()
    print("文件2:")
    print(' '.join(f'{b:02x}' for b in data2[:100]))

if __name__ == "__main__":
    file1 = "/workspace/IPX-967.mp4.vsmeta"
    file2 = "/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta"
    compare_files(file1, file2)
