"""
测试语言检测工具函数
"""
import pytest

from mdcx.utils.language import (
    is_japanese,
    is_english,
    is_probably_english_for_translation
)


class TestLanguageDetection:
    """测试语言检测功能"""

    def test_is_japanese_true(self):
        """测试检测日语（检测假名）"""
        assert is_japanese("こんにちは") is True
        assert is_japanese("アイウエオ") is True
        assert is_japanese("カタカナ") is True
        assert is_japanese("ABC かたかな") is True  # 包含假名

    def test_is_japanese_false(self):
        """测试非日语"""
        assert is_japanese("Hello") is False
        assert is_japanese("中文") is False
        assert is_japanese("123") is False
        assert is_japanese("") is False

    def test_is_english_true(self):
        """测试检测英语"""
        assert is_english("Hello World") is True
        assert is_english("Hello, World!") is True
        assert is_english("123 Test") is True
        assert is_english("It's a test") is True

    def test_is_english_false(self):
        """测试非英语"""
        assert is_english("中文") is False
        assert is_english("日本語") is False
        assert is_english("Hello 中文") is False

    def test_is_probably_english_for_translation_true(self):
        """测试可能需要翻译的英语文本"""
        assert is_probably_english_for_translation("Hello World") is True
        assert is_probably_english_for_translation("This is a test sentence.") is True
        assert is_probably_english_for_translation("Short text") is True
        assert is_probably_english_for_translation("AV Actress") is True

    def test_is_probably_english_for_translation_false(self):
        """测试不太可能是英语的文本"""
        assert is_probably_english_for_translation("") is False
        assert is_probably_english_for_translation("日本語") is False
        assert is_probably_english_for_translation("中文测试") is False
        assert is_probably_english_for_translation("ABC 中文混合") is False

    def test_is_probably_english_for_translation_mixed(self):
        """测试混合文本"""
        assert is_probably_english_for_translation("Japanese text 日本語") is False
        assert is_probably_english_for_translation("中文占大部分 English") is False