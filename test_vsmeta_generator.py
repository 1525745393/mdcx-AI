#!/usr/bin/env python3
"""测试 VSMETA 生成器 - 验证修复后的格式"""

import sys
sys.path.insert(0, '/workspace')

# 先导入并模拟依赖
from unittest.mock import MagicMock, patch
import io

# 创建模拟配置
mock_manager = MagicMock()
mock_manager.config.vsmeta_image_max_dimension = 1920
mock_manager.config.vsmeta_jpeg_quality = 90
mock_manager.config.vsmeta_locked = True
mock_manager.config.vsmeta_include_poster = True
mock_manager.config.vsmeta_include_backdrop = True
mock_manager.config.vsmeta_actor_limit = 20
mock_manager.config.vsmeta_tag_limit = 10

# 创建模拟信号
mock_signal = MagicMock()

# 创建模拟日志
mock_log = MagicMock()
mock_log.log.return_value = MagicMock()
mock_log.log.return_value.write = MagicMock()

# 模拟 PIL
mock_image = MagicMock()
mock_image.open.return_value.__enter__ = MagicMock(return_value=MagicMock(
    size=(100, 150),
    mode='RGB'
))
mock_image.open.return_value.__exit__ = MagicMock(return_value=False)

# 模拟 aiofiles
mock_aiofiles = MagicMock()

# 使用 patch 导入模块
with patch.dict('sys.modules', {
    'aiofiles': mock_aiofiles,
    'aiofiles.os': mock_aiofiles.os,
    'PIL': mock_image,
    'PIL.Image': mock_image,
}):
    with patch('mdcx.core.vsmeta.manager', mock_manager):
        with patch('mdcx.core.vsmeta.signal', mock_signal):
            with patch('mdcx.core.vsmeta.LogBuffer', mock_log):
                with patch('mdcx.core.vsmeta.delete_file_async', MagicMock()):
                    with patch('mdcx.core.vsmeta.move_file_async', MagicMock()):
                        # 现在导入 vsmeta 模块
                        from mdcx.core.vsmeta import VSMetaEncoder


def test_vsmeta_structure():
    """测试 VSMETA 结构是否正确"""
    print("=" * 60)
    print("测试 VSMETA 编码器结构")
    print("=" * 60)

    encoder = VSMetaEncoder()
    encoder.write_header()

    # 写入基本字段
    encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE, "[IPX-805] 测试标题", label="showTitle")
    encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE2, "Original Title", label="showTitle2")
    encoder.write_string_field(VSMetaEncoder.TAG_EPISODE_TITLE, "IPX-805", label="episodeTitle")
    encoder.write_varint_field(VSMetaEncoder.TAG_YEAR, 2022, label="year")
    encoder.write_string_field(VSMetaEncoder.TAG_EPISODE_RELEASE_DATE, "2022-02-08", label="releaseDate")
    encoder.write_varint_field(VSMetaEncoder.TAG_EPISODE_LOCKED, 1, label="locked")
    encoder.write_string_field(VSMetaEncoder.TAG_CHAPTER_SUMMARY, "测试剧情简介", label="summary")

    # GROUP1 - 演员/导演/类型
    def build_group1(sub):
        sub.write_string_field(VSMetaEncoder.TAG1_CAST, "演员A", label="cast")
        sub.write_string_field(VSMetaEncoder.TAG1_CAST, "演员B", label="cast")
        sub.write_string_field(VSMetaEncoder.TAG1_GENRE, "剧情", label="genre")

    encoder.write_submessage(VSMetaEncoder.TAG_GROUP1, build_group1, label="group1")

    # 分类
    encoder.write_string_field(VSMetaEncoder.TAG_CLASSIFICATION, "有码", label="classification")

    # 评分
    encoder.write_rating("8.5", label="rating")

    # GROUP2 - 系列信息
    def build_group2(sub):
        sub.write_varint_field(VSMetaEncoder.TAG2_SEASON, 0, label="season")
        sub.write_varint_field(VSMetaEncoder.TAG2_EPISODE, 0, label="episode")
        sub.write_varint_field(VSMetaEncoder.TAG2_TV_SHOW_YEAR, 2022, label="tvshowYear")
        sub.write_string_field(VSMetaEncoder.TAG2_RELEASE_DATE_TV_SHOW, "2022-02-08", label="tvshowReleaseDate")
        sub.write_varint_field(VSMetaEncoder.TAG2_LOCKED, 1, label="tvshowLocked")
        sub.write_string_field(VSMetaEncoder.TAG2_TVSHOW_SUMMARY, "系列名称", label="tvshowSummary")
        sub.write_string_field(
            VSMetaEncoder.TAG2_TVSHOW_META_JSON,
            VSMetaEncoder.DEFAULT_META_JSON,
            label="tvshowMetaJson"
        )

    # 关键修复：不使用 index=0x01
    encoder.write_submessage(VSMetaEncoder.TAG_GROUP2, build_group2, label="group2")

    # GROUP3 - 背景图 + 时间戳
    def build_group3(sub):
        sub.write_varint_field(VSMetaEncoder.TAG3_TIMESTAMP, 1609459200, label="timestamp")

    # 关键修复：不使用 index=0x01
    encoder.write_submessage(VSMetaEncoder.TAG_GROUP3, build_group3, label="group3")

    # 获取结果
    data = encoder.get_bytes()

    # 保存到文件
    output_path = "/workspace/test_output.vsmeta"
    with open(output_path, "wb") as f:
        f.write(data)

    print(f"\n✅ 生成成功！")
    print(f"文件大小: {len(data)} bytes")
    print(f"保存路径: {output_path}")

    # 验证结构
    print(f"\n{'='*60}")
    print("结构验证")
    print(f"{'='*60}")

    # 检查头部
    assert data[0] == 0x08 and data[1] == 0x01, "头部错误"
    print("✅ 文件头正确 (0x08 0x01)")

    # 检查关键字段是否存在
    tags_found = set()
    offset = 2
    while offset < len(data):
        tag = data[offset]
        tags_found.add(f"0x{tag:02X}")
        wire_type = tag & 0x07
        offset += 1

        if wire_type == 0:  # varint
            while offset < len(data) and data[offset] & 0x80:
                offset += 1
            offset += 1
        elif wire_type == 2:  # length-delimited
            length = 0
            shift = 0
            while offset < len(data):
                byte = data[offset]
                offset += 1
                length |= (byte & 0x7F) << shift
                if not (byte & 0x80):
                    break
                shift += 7
            offset += length

    expected_tags = ["0x12", "0x1A", "0x22", "0x28", "0x32", "0x38", "0x42", "0x52", "0x5A", "0x60", "0x9A", "0xAA"]
    for tag in expected_tags:
        if tag in tags_found:
            print(f"✅ 包含字段 {tag}")
        else:
            print(f"⚠️  缺少字段 {tag}")

    # 关键检查：验证没有错误的索引字节
    print(f"\n{'='*60}")
    print("关键修复验证")
    print(f"{'='*60}")

    # 检查 GROUP2 (0x9A) 后面是否没有 0x01 索引字节
    for i in range(len(data) - 1):
        if data[i] == 0x9A:
            next_byte = data[i + 1]
            if next_byte == 0x01:
                print(f"❌ 发现 GROUP2 后有错误的索引字节 0x01 (位置 {i})")
            else:
                print(f"✅ GROUP2 (0x9A) 后没有索引字节，正确")

        if data[i] == 0xAA:
            next_byte = data[i + 1]
            if next_byte == 0x01:
                print(f"❌ 发现 GROUP3 后有错误的索引字节 0x01 (位置 {i})")
            else:
                print(f"✅ GROUP3 (0xAA) 后没有索引字节，正确")

    # 检查海报字段 (0x8A) 后面是否没有 0x01 索引字节
    for i in range(len(data) - 1):
        if data[i] == 0x8A:
            next_byte = data[i + 1]
            if next_byte == 0x01:
                print(f"❌ 发现海报字段后有错误的索引字节 0x01 (位置 {i})")
            else:
                print(f"✅ 海报字段 (0x8A) 后没有索引字节，正确")

    print(f"\n{'='*60}")
    print("测试完成！")
    print(f"{'='*60}")

    return data


if __name__ == "__main__":
    test_vsmeta_structure()
