from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from mdcx.config.enums import VsmetaShowTitle, VsmetaShowTitle2, VsmetaSummary
from mdcx.core.vsmeta import (
    VSMetaEncoder,
    parse_release_date,
    parse_score,
    parse_runtime,
)


def _jpeg_bytes(size: tuple[int, int] = (200, 300)) -> bytes:
    output = BytesIO()
    Image.new("RGB", size, "white").save(output, format="JPEG")
    return output.getvalue()


class TestVSMetaEncoder:
    def test_initial_state(self):
        encoder = VSMetaEncoder()
        assert len(encoder.written_tags) == 0
        assert encoder.get_bytes() == b""

    def test_reset(self):
        encoder = VSMetaEncoder()
        encoder.write_header()
        assert len(encoder.get_bytes()) > 0

        encoder.reset()
        assert len(encoder.written_tags) == 0
        assert encoder.get_bytes() == b""

    def test_write_header(self):
        encoder = VSMetaEncoder()
        encoder.write_header()
        result = encoder.get_bytes()
        assert result == b"\x08\x01"
        assert len(encoder.written_tags) == 0

    def test_write_string_field(self):
        encoder = VSMetaEncoder()
        encoder.write_string_field(0x12, "Test Title", label="showTitle")
        result = encoder.get_bytes()
        assert len(result) > 0
        assert "showTitle" in encoder.written_tags

    def test_write_string_field_empty(self):
        encoder = VSMetaEncoder()
        encoder.write_string_field(0x12, "", label="showTitle")
        result = encoder.get_bytes()
        assert len(result) == 0
        assert len(encoder.written_tags) == 0

    def test_write_varint_field(self):
        encoder = VSMetaEncoder()
        encoder.write_varint_field(0x28, 2024, label="year")
        result = encoder.get_bytes()
        assert len(result) > 0
        assert "year" in encoder.written_tags

    def test_normalize_vsmeta_text(self):
        test_cases = [
            ("", ""),
            ("Test &amp; &lt; &gt;", "Test & < >"),
            ("Line1\r\nLine2", "Line1\nLine2"),
            ("Line1<br/>Line2", "Line1\nLine2"),
            ("Line1<br />Line2", "Line1\nLine2"),
            ("Text with \x00\x01\x02 control chars", "Text with  control chars"),
            ("Normal text with 日本語", "Normal text with 日本語"),
        ]

        for input_text, expected in test_cases:
            result = VSMetaEncoder.normalize_vsmeta_text(input_text)
            assert result == expected

    def test_encode_rating(self):
        assert VSMetaEncoder._encode_rating(None) == b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"
        assert VSMetaEncoder._encode_rating(0) == b"\x00"
        assert VSMetaEncoder._encode_rating(50) == b"\x32"
        assert VSMetaEncoder._encode_rating(100) == b"\x64"

    def test_write_rating(self):
        encoder = VSMetaEncoder()
        encoder.write_rating("8.5", label="rating")
        result = encoder.get_bytes()
        assert len(result) > 0
        assert "rating" in encoder.written_tags

    def test_write_rating_none(self):
        encoder = VSMetaEncoder()
        encoder.write_rating("N/A", label="rating")
        result = encoder.get_bytes()
        assert len(result) > 0
        assert len(encoder.written_tags) == 0

    def test_write_submessage(self):
        encoder = VSMetaEncoder()

        def build_sub(sub):
            sub.write_string_field(0x0A, "Actor Name", label="cast")

        encoder.write_submessage(0x52, build_sub, label="group1")
        result = encoder.get_bytes()
        assert len(result) > 0
        assert "group1" in encoder.written_tags
        assert "cast" in encoder.written_tags

    def test_full_encoding_flow(self, tmp_path):
        encoder = VSMetaEncoder()
        encoder.write_header()
        encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE, "Test Title", label="showTitle")
        encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE2, "Original Title", label="showTitle2")
        encoder.write_varint_field(VSMetaEncoder.TAG_YEAR, 2024, label="year")
        encoder.write_string_field(VSMetaEncoder.TAG_CHAPTER_SUMMARY, "Test summary", label="summary")

        result = encoder.get_bytes()
        assert len(result) > 0
        assert "showTitle" in encoder.written_tags
        assert "showTitle2" in encoder.written_tags
        assert "year" in encoder.written_tags
        assert "summary" in encoder.written_tags

    def test_encode_image(self, tmp_path):
        img_path = tmp_path / "test.jpg"
        with open(img_path, "wb") as f:
            f.write(_jpeg_bytes())

        b64_data, md5_hex = VSMetaEncoder._encode_image(img_path, 400, 85)
        assert b64_data is not None
        assert md5_hex is not None
        assert len(b64_data) > 0
        assert len(md5_hex) == 32

    def test_encode_image_nonexistent(self, tmp_path):
        img_path = tmp_path / "nonexistent.jpg"
        b64_data, md5_hex = VSMetaEncoder._encode_image(img_path, 400, 85)
        assert b64_data is None
        assert md5_hex is None


class TestParseHelpers:
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("2024-01-15", (2024, 1, 15)),
            ("2024/1/5", (2024, 1, 5)),
            ("2024-12-31", (2024, 12, 31)),
            ("", None),
            (None, None),
            ("invalid", None),
            ("2024/xx/xx", None),
        ],
    )
    def test_parse_release_date(self, input_str, expected):
        result = parse_release_date(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("8.5", 85),
            ("10", 100),
            ("0", 0),
            ("7.5分", 75),
            ("评分 9.2", 92),
            ("⭐8.5", 85),
            ("N/A", None),
            ("", None),
            (None, None),
            ("11", None),
            ("-1", None),
            ("invalid", None),
        ],
    )
    def test_parse_score(self, input_str, expected):
        result = parse_score(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("120", 120),
            ("120min", 120),
            ("120分钟", 120),
            ("2h", 120),
            ("2h 30m", 150),
            ("2小时30分钟", 150),
            ("1小时", 60),
            ("1时30分", 90),
            ("", None),
            (None, None),
            ("invalid", None),
        ],
    )
    def test_parse_runtime(self, input_str, expected):
        result = parse_runtime(input_str)
        assert result == expected


class TestConfigEnums:
    def test_vsmeta_show_title_names(self):
        names = VsmetaShowTitle.names()
        assert isinstance(names, list)
        assert len(names) == 2

    def test_vsmeta_show_title2_names(self):
        names = VsmetaShowTitle2.names()
        assert isinstance(names, list)
        assert len(names) == 4

    def test_vsmeta_summary_names(self):
        names = VsmetaSummary.names()
        assert isinstance(names, list)
        assert len(names) == 7
