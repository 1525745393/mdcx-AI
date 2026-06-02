"""
测试 LEB128 编码工具函数
"""
import pytest

from mdcx.utils.leb128 import (
    encode_leb128,
    encode_varint,
    decode_leb128,
    encode_string,
    encode_boolean,
    encode_int,
    encode_date
)


class TestLeb128Encoding:
    """测试 LEB128 编码功能"""

    def test_encode_leb128_small(self):
        """测试编码小整数"""
        assert encode_leb128(0) == b'\x00'
        assert encode_leb128(1) == b'\x01'
        assert encode_leb128(127) == b'\x7f'

    def test_encode_leb128_large(self):
        """测试编码大整数"""
        assert encode_leb128(128) == b'\x80\x01'
        assert encode_leb128(256) == b'\x80\x02'
        assert encode_leb128(300) == b'\xac\x02'
        assert encode_leb128(16383) == b'\xff\x7f'

    def test_encode_varint_alias(self):
        """测试 varint 别名"""
        assert encode_varint(128) == encode_leb128(128)

    def test_decode_leb128(self):
        """测试解码 LEB128"""
        assert decode_leb128(b'\x00') == (0, 1)
        assert decode_leb128(b'\x01') == (1, 1)
        assert decode_leb128(b'\x7f') == (127, 1)
        assert decode_leb128(b'\x80\x01') == (128, 2)
        assert decode_leb128(b'\xac\x02') == (300, 2)

    def test_decode_leb128_with_offset(self):
        """测试带偏移量的解码"""
        data = b'\x00\x80\x01\x7f'
        assert decode_leb128(data, 1) == (128, 3)
        assert decode_leb128(data, 3) == (127, 4)


class TestStringEncoding:
    """测试字符串编码功能"""

    def test_encode_string(self):
        """测试编码字符串"""
        result = encode_string("test")
        assert result == b'\x04test'

    def test_encode_string_empty(self):
        """测试编码空字符串"""
        assert encode_string("") == b'\x00'

    def test_encode_string_unicode(self):
        """测试编码Unicode字符串"""
        result = encode_string("日本語")
        assert len(result) == 1 + 9  # 1 byte length + 3 chars * 3 bytes UTF-8


class TestBooleanEncoding:
    """测试布尔值编码功能"""

    def test_encode_boolean(self):
        """测试编码布尔值"""
        assert encode_boolean(True) == b'\x01'
        assert encode_boolean(False) == b'\x00'


class TestIntEncoding:
    """测试整数编码功能"""

    def test_encode_int(self):
        """测试编码整数"""
        assert encode_int(42) == b'\x2a'
        assert encode_int(1000) == b'\xe8\x07'


class TestDateEncoding:
    """测试日期编码功能"""

    def test_encode_date(self):
        """测试编码日期"""
        result = encode_date(2024, 1, 15)
        expected = encode_string("2024-01-15")
        assert result == expected

    def test_encode_date_with_leading_zeros(self):
        """测试带前导零的日期"""
        result = encode_date(2024, 2, 8)
        expected = encode_string("2024-02-08")
        assert result == expected