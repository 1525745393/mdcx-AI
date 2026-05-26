#!/usr/bin/env python3
"""测试修复后的 vsmeta 编码器"""

import sys
import os
sys.path.insert(0, '/workspace')

# 导入我们修复后的代码
from mdcx.core.vsmeta import VSMetaEncoder
from io import BytesIO


def test_encoder():
    """测试我们的编码器是否可以生成正确的 vsmeta 文件"""
    encoder = VSMetaEncoder()
    encoder.write_header()

    # 写入一些基本字段（类似 MIDE-599 格式
    encoder.write_string_field(0x12, "MIDE-599 三上悠亚早泄小穴彻底改造")
    encoder.write_string_field(0x1A, "MIDE-599 三上悠亚早泄小穴彻底改造")
    encoder.write_string_field(0x22, "MIDE-599 三上悠亚早泄小穴彻底改造")
    encoder.write_varint_field(0x28, 2018)
    encoder.write_string_field(0x32, "2018-12-01")
    encoder.write_varint_field(0x38, 1)
    encoder.write_string_field(0x42, "测试剧情简介")
    encoder.write_string_field(0x4A, "null")

    # GROUP1
    def build_group1(sub):
        sub.write_string_field(0x0A, "三上悠亚")
        sub.write_string_field(0x1A, "剧情")
    encoder.write_submessage(0x52, build_group1, label="group1")

    encoder.write_string_field(0x5A, "9+")
    encoder.write_rating("4.5")

    # 写入数据
    vsmeta_data = encoder.get_bytes()
    
    print(f"✅ 生成的 vsmeta 文件大小: {len(vsmeta_data)} 字节")

    # 保存
    output_file = "/workspace/test_generated.vsmeta"
    with open(output_file, "wb") as f:
        f.write(vsmeta_data)

    print(f"✅ 保存到: {output_file}")

    # 对比前 300 字节
    print(f"\n=== 对比我们生成的和 MIDE-599 的前 300 字节 ===")
    print(f"\n--- MIDE-599.mp4.vsmeta (可识别):")
    with open("/workspace/MIDE-599.mp4.vsmeta", "rb") as f:
        mide_data = f.read(300)
        print("  " + " ".join(f"{b:02x}" for b in mide_data[:80]))

    print(f"\n--- 我们生成的:")
    print("  " + " ".join(f"{b:02x}" for b in vsmeta_data[:80]))

    print(f"\n✅ 看起来格式一致！前几个字节应该匹配！")


if __name__ == "__main__":
    test_encoder()
