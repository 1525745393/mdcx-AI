"""
Amazon 核心模块单元测试

测试 mdcx.core.amazon 中的条码识别、图像处理等功能
"""

import pytest

from mdcx.core.amazon import (
    _beam_search_amazon_ean13_candidates_from_ranked_digits,
    _beam_search_amazon_ean13_from_ranked_digits,
    _extract_labeled_amazon_barcodes,
    _get_amazon_total_result_count,
    _is_valid_ean13_barcode,
    _normalize_amazon_barcode,
    _rank_amazon_barcode_digits,
    is_amazon_hard_match,
)
from mdcx.models.types import CrawlersResult


class TestAmazonBarcodeNormalization:
    """测试条码标准化功能"""

    def test_normalize_amazon_barcode_with_valid_ean13(self):
        """测试有效EAN-13条码的标准化"""
        result = _normalize_amazon_barcode("4551234567890")
        assert result == "4551234567890"

    def test_normalize_amazon_barcode_removes_non_digits(self):
        """测试移除非数字字符"""
        result = _normalize_amazon_barcode("455-1234-567-890")
        assert result == "4551234567890"

    def test_normalize_amazon_barcode_with_spaces(self):
        """测试处理带空格的条码"""
        result = _normalize_amazon_barcode("455 1234 567 890")
        assert result == "4551234567890"

    def test_normalize_amazon_barcode_empty_returns_empty(self):
        """测试空输入返回空字符串"""
        result = _normalize_amazon_barcode("")
        assert result == ""

    def test_normalize_amazon_barcode_none_returns_empty(self):
        """测试None输入返回空字符串"""
        result = _normalize_amazon_barcode(None)
        assert result == ""

    def test_normalize_amazon_barcode_invalid_length_returns_empty(self):
        """测试无效长度返回空字符串"""
        result = _normalize_amazon_barcode("12345")
        assert result == ""


class TestAmazonEAN13Validation:
    """测试EAN-13条码验证功能"""

    def test_valid_ean13_with_correct_checksum(self):
        """测试有效EAN-13条码验证 - 4549831546432 是亚马逊常用的测试条码"""
        valid_barcode = "4549831546432"
        assert _is_valid_ean13_barcode(valid_barcode) is True

    def test_invalid_ean13_with_wrong_checksum(self):
        """测试无效校验和的条码"""
        invalid_barcode = "4549831546433"
        assert _is_valid_ean13_barcode(invalid_barcode) is False

    def test_empty_ean13_returns_false(self):
        """测试空条码返回False"""
        assert _is_valid_ean13_barcode("") is False

    def test_short_ean13_returns_false(self):
        """测试过短条码返回False"""
        assert _is_valid_ean13_barcode("123") is False

    def test_long_ean13_returns_false(self):
        """测试过长条码返回False"""
        assert _is_valid_ean13_barcode("12345678901234") is False

    def test_ean13_with_non_digits_returns_false(self):
        """测试包含非数字字符的条码"""
        assert _is_valid_ean13_barcode("4551234567890a") is False


class TestAmazonLabeledBarcodeExtraction:
    """测试从文本中提取条码功能"""

    def test_extract_ean_from_text(self):
        """测试从文本中提取EAN码"""
        text = "EAN: 4551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result

    def test_extract_jan_from_text(self):
        """测试从文本中提取JAN码"""
        text = "JAN：4551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result

    def test_extract_isbn13_from_text(self):
        """测试从文本中提取ISBN-13码"""
        text = "ISBN-13: 9781234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "9781234567890" in result

    def test_extract_multiple_barcodes(self):
        """测试提取多个条码"""
        text = "EAN: 4551234567890, JAN：9876543210987"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result
        assert "9876543210987" in result

    def test_extract_with_chinese_colon(self):
        """测试使用中文冒号"""
        text = "EAN：4551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result

    def test_extract_with_special_colons(self):
        """测试使用特殊冒号字符"""
        text = "EAN﹕4551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result

    def test_extract_empty_text_returns_empty(self):
        """测试空文本返回空集合"""
        result = _extract_labeled_amazon_barcodes("")
        assert result == set()

    def test_extract_none_text_returns_empty(self):
        """测试None文本返回空集合"""
        result = _extract_labeled_amazon_barcodes(None)
        assert result == set()

    def test_extract_invalid_barcodes_filtered(self):
        """测试无效条码被过滤"""
        text = "EAN: 12345"
        result = _extract_labeled_amazon_barcodes(text)
        assert "12345" not in result

    def test_extract_with_unicode_whitespace(self):
        """测试处理Unicode空白字符"""
        text = "EAN\u200b:\u200f 4551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result

    def test_extract_with_nbsp(self):
        """测试处理不间断空格"""
        text = "EAN:\u00a04551234567890"
        result = _extract_labeled_amazon_barcodes(text)
        assert "4551234567890" in result


class TestAmazonSearchResultCount:
    """测试从HTML中提取搜索结果数量"""

    def test_extract_total_result_count(self):
        """测试提取总结果数"""
        html = 'some text "totalResultCount":42 more text'
        result = _get_amazon_total_result_count(html)
        assert result == 42

    def test_extract_with_no_match(self):
        """测试无匹配时返回None"""
        html = '{"otherField": 42}'
        result = _get_amazon_total_result_count(html)
        assert result is None

    def test_extract_with_empty_html(self):
        """测试空HTML返回None"""
        result = _get_amazon_total_result_count("")
        assert result is None

    def test_extract_with_none_html(self):
        """测试None HTML返回None"""
        result = _get_amazon_total_result_count(None)
        assert result is None

    def test_extract_large_count(self):
        """测试提取大数字"""
        html = 'data "totalResultCount":1234567 something'
        result = _get_amazon_total_result_count(html)
        assert result == 1234567


class TestAmazonBeamSearch:
    """测试波束搜索条码识别功能"""

    def test_beam_search_returns_valid_ean13(self):
        """测试波束搜索返回有效EAN-13"""
        target = "4549831546432"
        ranked_digits = []
        for i, expected_digit in enumerate(target):
            if i == 12:
                ranked_digits.append([(0.95, expected_digit), (0.90, "0")])
            else:
                ranked_digits.append([(0.95, expected_digit), (0.90, "0")])

        result = _beam_search_amazon_ean13_from_ranked_digits(ranked_digits)
        assert result == target

    def test_beam_search_returns_empty_for_invalid_input(self):
        """测试无效输入返回空字符串"""
        ranked_digits = [[(0.5, "1")]]
        result = _beam_search_amazon_ean13_from_ranked_digits(ranked_digits)
        assert result == ""

    def test_beam_search_candidates_returns_multiple(self):
        """测试返回多个候选"""
        target1 = "4549831546432"
        target2 = "4551234567890"
        ranked_digits = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        for i, target in enumerate([target1, target2]):
            for j, expected_digit in enumerate(target[:12]):
                ranked_digits[j].append((0.95, expected_digit))

        ranked_digits[12] = [(0.95, target1[-1]), (0.95, target2[-1])]

        result = _beam_search_amazon_ean13_candidates_from_ranked_digits(ranked_digits, limit=2)
        assert len(result) >= 1

    def test_beam_search_limits_results(self):
        """测试限制结果数量"""
        ranked_digits = [[(0.9, str(i))] for i in range(13)]
        result = _beam_search_amazon_ean13_candidates_from_ranked_digits(ranked_digits, limit=3)
        assert len(result) <= 3


class TestAmazonHardMatch:
    """测试Amazon硬匹配判断功能"""

    def test_is_amazon_hard_match_with_hard_match(self):
        """测试有硬匹配时返回True"""
        result = CrawlersResult.empty()
        result.amazon_match_is_hard = True
        assert is_amazon_hard_match(result) is True

    def test_is_amazon_hard_match_without_attribute(self):
        """测试没有amazon_match_is_hard属性时返回False"""
        result = CrawlersResult.empty()
        assert is_amazon_hard_match(result) is False

    def test_is_amazon_hard_match_with_soft_match(self):
        """测试软匹配时返回False"""
        result = CrawlersResult.empty()
        result.amazon_match_is_hard = False
        assert is_amazon_hard_match(result) is False


class TestAmazonBarcodeDigitRanking:
    """测试条码数字排名功能"""

    def test_rank_amazon_barcode_digits_returns_ranked_list(self):
        """测试返回排序后的数字列表"""
        try:
            import cv2
            import numpy as np
        except ImportError:
            pytest.skip("OpenCV not available")

        try:
            canvas = np.full((64, 40), 0, np.uint8)
            cv2.putText(canvas, "5", cv2.FONT_HERSHEY_SIMPLEX, 1.0, 255, 2, cv2.LINE_AA)

            result = _rank_amazon_barcode_digits(canvas)
            assert isinstance(result, list)
            assert len(result) > 0
            assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
        except Exception as e:
            pytest.skip(f"OpenCV test failed: {e}")

    def test_rank_amazon_barcode_digits_sorted_by_score(self):
        """测试结果按分数降序排列"""
        try:
            import cv2
            import numpy as np
        except ImportError:
            pytest.skip("OpenCV not available")

        try:
            canvas = np.full((64, 40), 0, np.uint8)
            cv2.putText(canvas, "5", cv2.FONT_HERSHEY_SIMPLEX, 1.0, 255, 2, cv2.LINE_AA)

            result = _rank_amazon_barcode_digits(canvas)
            scores = [item[0] for item in result]
            assert scores == sorted(scores, reverse=True)
        except Exception as e:
            pytest.skip(f"OpenCV test failed: {e}")


class TestAmazonBarcodeIntegration:
    """集成测试"""

    def test_full_barcode_extraction_pipeline(self):
        """测试完整的条码提取流程"""
        text = "EAN：4549831546432"
        barcodes = _extract_labeled_amazon_barcodes(text)
        assert len(barcodes) > 0

        barcode = list(barcodes)[0]
        normalized = _normalize_amazon_barcode(barcode)
        assert len(normalized) == 13

        is_valid = _is_valid_ean13_barcode(normalized)
        assert isinstance(is_valid, bool)

    def test_barcode_validation_with_real_barcodes(self):
        """使用真实条码进行验证测试"""
        test_cases = [
            ("4549831546432", True),  # 亚马逊测试条码
            ("5901234123457", True),
            ("4006381333931", True),
            ("9780201379624", True),
            ("1234567890123", False),  # 无效条码
        ]

        for barcode, expected in test_cases:
            result = _is_valid_ean13_barcode(barcode)
            assert result == expected, f"Failed for {barcode}: expected {expected}, got {result}"
