import base64
import hashlib
import json
import time
import traceback
from io import BytesIO
from pathlib import Path

import aiofiles
from PIL import Image

from ..config.enums import DownloadableFile, KeepableFile, ReadMode, Switch
from ..config.manager import manager
from ..config.resource_policy import resource_policy
from ..models.log_buffer import LogBuffer
from ..models.types import CrawlersResult, FileInfo
from ..signals import signal
from ..utils import get_used_time
from ..utils.file import delete_file_async, move_file_async
from ..utils.leb128 import encode_varint


class VSMetaEncoder:
    """VSMETA protobuf encoder for Synology Video Station

    Implements the real Synology VSMETA binary format based on reverse engineering
    by soywiz / Carlos Ballesteros Velasco. The format uses protobuf-style encoding:
      - tag_byte = (field_number << 3) | wire_type
      - wire_type 0 = varint, wire_type 2 = length-delimited
      - Sub-messages use nested groups (GROUP1, GROUP2, GROUP3)
      - Images are Base64-encoded with MD5 checksums
    """

    # File header: field 1 (wire 0) = content type (1=movie, 2=series, 3=other)
    HEADER_MOVIE = b"\x08\x01"

    # ── Top-level tags ──
    TAG_SHOW_TITLE = 0x12  # field 2, wire 2 (str)
    TAG_SHOW_TITLE2 = 0x1A  # field 3, wire 2 (str) — sort/alt title
    TAG_EPISODE_TITLE = 0x22  # field 4, wire 2 (str) — short title
    TAG_YEAR = 0x28  # field 5, wire 0 (varint)
    TAG_EPISODE_RELEASE_DATE = 0x32  # field 6, wire 2 (str "yyyy-MM-dd")
    TAG_EPISODE_LOCKED = 0x38  # field 7, wire 0 (bool varint)
    TAG_CHAPTER_SUMMARY = 0x42  # field 8, wire 2 (str)
    TAG_EPISODE_META_JSON = 0x4A  # field 9, wire 2 (str JSON)
    TAG_GROUP1 = 0x52  # field 10, wire 2 (sub-message: cast/crew/genre)
    TAG_CLASSIFICATION = 0x5A  # field 11, wire 2 (str)
    TAG_RATING = 0x60  # field 12, wire 0 (special: 1B or 10B)
    TAG_EPISODE_THUMB_DATA = 0x8A  # field 17, wire 2 (str, Base64 image)
    TAG_EPISODE_THUMB_MD5 = 0x92  # field 18, wire 2 (str, MD5 hex)
    TAG_GROUP2 = 0x9A  # field 19, wire 2 (sub-message: series info + poster)
    TAG_GROUP3 = 0xAA  # field 21, wire 2 (sub-message: backdrop + timestamp, movies)

    # ── GROUP1 internal tags (cast / crew / genre) ──
    TAG1_CAST = 0x0A  # field 1, wire 2 (str, repeated)
    TAG1_DIRECTOR = 0x12  # field 2, wire 2 (str, repeated)
    TAG1_GENRE = 0x1A  # field 3, wire 2 (str, repeated)
    TAG1_WRITER = 0x22  # field 4, wire 2 (str, repeated)

    # ── GROUP2 internal tags (series-level info) ──
    TAG2_SEASON = 0x08  # field 1, wire 0 (varint)
    TAG2_EPISODE = 0x10  # field 2, wire 0 (varint)
    TAG2_TV_SHOW_YEAR = 0x18  # field 3, wire 0 (varint)
    TAG2_RELEASE_DATE_TV_SHOW = 0x22  # field 4, wire 2 (str)
    TAG2_LOCKED = 0x28  # field 5, wire 0 (bool varint)
    TAG2_TVSHOW_SUMMARY = 0x32  # field 6, wire 2 (str)
    TAG2_POSTER_DATA = 0x3A  # field 7, wire 2 (str, Base64 image)
    TAG2_POSTER_MD5 = 0x42  # field 8, wire 2 (str, MD5 hex)
    TAG2_TVSHOW_META_JSON = 0x4A  # field 9, wire 2 (str JSON)

    # ── GROUP3 internal tags (backdrop + timestamp) ──
    TAG3_BACKDROP_DATA = 0x0A  # field 1, wire 2 (str, Base64 image)
    TAG3_BACKDROP_MD5 = 0x12  # field 2, wire 2 (str, MD5 hex)
    TAG3_TIMESTAMP = 0x18  # field 3, wire 0 (varint, unix seconds)

    # Default JSON for meta fields (required by Video Station)
    DEFAULT_META_JSON = '{"com.synology.FileAssets":{}}'

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset encoder to initial state for reuse"""
        self.buffer = BytesIO()
        self.written_tags: list[str] = []

    def _track(self, tag_name: str):
        """Record that a tag was successfully written"""
        self.written_tags.append(tag_name)

    # ── Protobuf wire-type writers ──

    def write_header(self):
        """Write VSMETA file header (content type = movie)"""
        self.buffer.write(self.HEADER_MOVIE)

    def write_varint_field(self, tag: int, value: int, label: str | None = None):
        """Write a protobuf varint field (wire type 0): tag_byte + varint(value)"""
        self.buffer.write(bytes([tag]))
        self.buffer.write(encode_varint(value))
        if label:
            self._track(label)

    def write_bytes_field(self, tag: int, data: bytes, label: str | None = None):
        """Write a protobuf length-delimited field (wire type 2): tag_byte + varint(len) + data"""
        self.buffer.write(bytes([tag]))
        self.buffer.write(encode_varint(len(data)))
        self.buffer.write(data)
        if label:
            self._track(label)

    def write_string_field(self, tag: int, value: str, label: str | None = None):
        """Write a string as a protobuf length-delimited field"""
        if value:
            self.write_bytes_field(tag, value.encode("utf-8"), label=label)

    def write_indexed_string_field(self, tag: int, index: int, value: str, label: str | None = None):
        """Write a length-delimited field with a 1-byte index between tag and payload"""
        data = value.encode("utf-8")
        self.buffer.write(bytes([tag]))
        self.buffer.write(bytes([index]))
        self.buffer.write(encode_varint(len(data)))
        self.buffer.write(data)
        if label:
            self._track(label)

    def write_submessage(self, tag: int, build_func, label: str | None = None, index: int | None = None):
        """Write a nested sub-message group

        build_func is called with a temporary encoder to populate the sub-message.
        The result is written as a length-delimited field.

        If index is provided, an index byte is inserted after the tag byte
        (used by GROUP2 0x9A and GROUP3 0xAA).
        """
        sub = VSMetaEncoder()
        sub.write_header = lambda: None  # suppress header in sub-messages
        build_func(sub)
        payload = sub.get_bytes()

        self.buffer.write(bytes([tag]))
        if index is not None:
            self.buffer.write(bytes([index]))
        self.buffer.write(encode_varint(len(payload)))
        self.buffer.write(payload)

        # Merge written tags from sub-message
        if label:
            self._track(label)
        self.written_tags.extend(sub.written_tags)

    # ── Image encoding ──

    @staticmethod
    def _encode_image(image_path: Path, max_dim: int, quality: int) -> tuple[str, str] | tuple[None, None]:
        """Encode image to Base64 string (76-char line-wrapped) and MD5 hex digest

        Returns (base64_data, md5_hex) or (None, None) on failure.
        """
        try:
            with Image.open(image_path) as img:
                if max(img.size) > max_dim:
                    ratio = max_dim / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.LANCZOS)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                buf = BytesIO()
                img.save(buf, format="JPEG", quality=quality)
                raw = buf.getvalue()

            md5_hex = hashlib.md5(raw).hexdigest()
            b64 = base64.b64encode(raw).decode("ascii")
            # Wrap at 76 characters per line
            b64_wrapped = "\n".join(b64[i : i + 76] for i in range(0, len(b64), 76))
            return b64_wrapped, md5_hex
        except Exception:
            LogBuffer.log().write(f"\n ⚠️ VSMETA image encode failed: {image_path}")
            signal.show_traceback_log(traceback.format_exc())
            return None, None

    def write_poster(self, image_path: Path | None, label: str = "poster"):
        """Write episode thumbnail (poster) with Base64 data + MD5"""
        if not image_path or not image_path.exists():
            return
        max_dim = manager.config.vsmeta_image_max_dimension
        quality = manager.config.vsmeta_jpeg_quality
        b64_data, md5_hex = self._encode_image(image_path, max_dim, quality)
        if b64_data is None:
            return
        self.write_indexed_string_field(self.TAG_EPISODE_THUMB_DATA, 0x01, b64_data, label=label)
        self.write_indexed_string_field(self.TAG_EPISODE_THUMB_MD5, 0x01, md5_hex, label=f"{label}_md5")

    def write_poster_in_group2(self, image_path: Path | None, label: str = "poster_g2"):
        """Write poster image inside GROUP2 (without index byte)"""
        if not image_path or not image_path.exists():
            return
        max_dim = manager.config.vsmeta_image_max_dimension
        quality = manager.config.vsmeta_jpeg_quality
        b64_data, md5_hex = self._encode_image(image_path, max_dim, quality)
        if b64_data is None:
            return
        self.write_string_field(self.TAG2_POSTER_DATA, b64_data, label=label)
        self.write_string_field(self.TAG2_POSTER_MD5, md5_hex, label=f"{label}_md5")

    def write_backdrop_in_group3(self, image_path: Path | None, label: str = "backdrop"):
        """Write backdrop image inside GROUP3 (without index byte)"""
        if not image_path or not image_path.exists():
            return
        max_dim = manager.config.vsmeta_image_max_dimension
        quality = manager.config.vsmeta_jpeg_quality
        b64_data, md5_hex = self._encode_image(image_path, max_dim, quality)
        if b64_data is None:
            return
        self.write_string_field(self.TAG3_BACKDROP_DATA, b64_data, label=label)
        self.write_string_field(self.TAG3_BACKDROP_MD5, md5_hex, label=f"{label}_md5")

    # ── Rating encoding ──

    @staticmethod
    def _encode_rating(rating: int | None) -> bytes:
        """Encode rating value for TAG_RATING (0x60)

        Non-negative: single big-endian byte (rating value, 0-100).
        None (no rating): 10-byte two's complement varint for -1.
        """
        if rating is None:
            return b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"
        return bytes([rating])

    def write_rating(self, score_str: str, label: str = "rating"):
        """Write rating field with proper encoding"""
        rating = parse_score(score_str)
        value_bytes = self._encode_rating(rating)
        self.buffer.write(bytes([self.TAG_RATING]))
        self.buffer.write(value_bytes)
        if rating is not None:
            self._track(label)

    def get_bytes(self) -> bytes:
        """Get the final VSMETA bytes"""
        return self.buffer.getvalue()


# ══════════════════════════════════════════════════
# Parse helpers (unchanged from previous version)
# ══════════════════════════════════════════════════


def parse_release_date(release_str: str) -> tuple[int, int, int] | None:
    """Parse release date string (YYYY-MM-DD), returns None if unparseable

    Handles: '2020-01-01', '2020-1-1', '2020/01/01', etc.
    """
    import re

    try:
        if not release_str:
            return None
        raw = str(release_str).strip()
        m = re.match(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", raw)
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
    except (ValueError, IndexError):
        pass
    return None


def parse_score(score: str) -> int | None:
    """Parse score string to VSMETA rating (0-100), returns None if unparseable

    Handles: '8.5', '8.5分', '⭐8.5', '评分 8.5', etc.
    """
    import re

    try:
        raw = str(score).strip()
        if not raw or raw.upper() in ("N/A", "NA", "NULL", "NONE", "-"):
            return None
        num_match = re.search(r"(\d+\.?\d*)", raw)
        if not num_match:
            return None
        value = float(num_match.group(1))
        if value < 0 or value > 10:
            return None
        return int(value * 10)
    except (ValueError, TypeError):
        return None


def parse_runtime(runtime: str) -> int | None:
    """Parse runtime string to minutes, returns None if unparseable

    Handles: '120', '120min', '120分钟', '2h', '1h30m', '90 mins',
             '1小时30分钟', '1小时', '1时30分', etc.
    """
    import re

    try:
        raw = str(runtime).strip()
        if not raw:
            return None

        raw = re.sub(r"(小时|時|时)\s*", "h", raw)
        raw = re.sub(r"(分钟|分)\s*", "m", raw)

        h_m_match = re.match(r"(\d+)\s*h\s*(\d+)\s*m", raw, re.IGNORECASE)
        if h_m_match:
            return int(h_m_match.group(1)) * 60 + int(h_m_match.group(2))

        h_match = re.match(r"(\d+)\s*h", raw, re.IGNORECASE)
        if h_match:
            return int(h_match.group(1)) * 60

        cleaned = re.sub(r"m\w*", "", raw, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        if cleaned:
            return int(float(cleaned))
        return None
    except (ValueError, TypeError):
        return None


def should_update_vsmeta(
    main_mode: int,
    switch_on: list[Switch],
    download_files: list[DownloadableFile],
    keep_files: list[KeepableFile],
    is_nfo_existed: bool,
    read_mode: list[ReadMode],
) -> bool:
    """Determine whether VSMETA should be written based on current mode and config

    Returns True if VSMETA should be generated/updated, False otherwise.
    """
    if main_mode == 2 and Switch.SORT_DEL in switch_on:
        return False

    if main_mode in [1, 2, 3] or (main_mode == 4 and not is_nfo_existed and ReadMode.NO_NFO_SCRAPE in read_mode):
        if DownloadableFile.VSMETA not in download_files:
            return False
        if KeepableFile.VSMETA in keep_files and is_nfo_existed:
            return False
        return True

    if main_mode == 4:
        if is_nfo_existed and ReadMode.HAS_NFO_UPDATE in read_mode and ReadMode.READ_UPDATE_NFO in read_mode:
            return True
        return False

    return True


async def write_vsmeta(
    file_info: FileInfo,
    data: CrawlersResult,
    vsmeta_file: Path,
    output_dir: Path,
    poster_path: Path | None = None,
    backdrop_path: Path | None = None,
    update: bool = True,
) -> bool:
    """Generate and write VSMETA file for Synology Video Station

    Uses the protobuf-based VSMETA binary format reverse-engineered from
    Synology Video Station. Supports both movie and series content types.

    Args:
        file_info: File information
        data: Crawled metadata
        vsmeta_file: Output VSMETA file path
        output_dir: Output directory
        poster_path: Path to poster image
        backdrop_path: Path to backdrop/fanart image
        update: Whether to update existing VSMETA
    """
    start_time = time.time()
    download_files = manager.config.download_files
    keep_files = manager.config.keep_files

    vsmeta_policy = resource_policy(
        DownloadableFile.VSMETA,
        KeepableFile.VSMETA,
        download_files=download_files,
        keep_files=keep_files,
    )

    if not update:
        if not vsmeta_policy.should_download:
            if not vsmeta_policy.should_keep and await aiofiles.os.path.exists(vsmeta_file):
                await delete_file_async(vsmeta_file)
            return True
        LogBuffer.log().write(f"\n 🍀 VSMETA done! (old)({get_used_time(start_time)}s)")
        return True

    try:
        if not await aiofiles.os.path.exists(output_dir):
            await aiofiles.os.makedirs(output_dir)

        encoder = VSMetaEncoder()
        encoder.write_header()

        # ── 1. TAG_SHOW_TITLE (0x12): Display title ──
        if data.title and data.number:
            display_title = f"[{data.number}] {data.title}"
        elif data.title:
            display_title = data.title
        elif data.number:
            display_title = data.number
        else:
            display_title = file_info.file_name

        if data.originaltitle and data.originaltitle != data.title:
            display_title += f" ({data.originaltitle})"

        encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE, display_title, label="showTitle")

        # ── 2. TAG_SHOW_TITLE2 (0x1A): Sort / alternative title ──
        show_title2 = data.originaltitle or data.studio or data.publisher or ""
        encoder.write_string_field(VSMetaEncoder.TAG_SHOW_TITLE2, show_title2, label="showTitle2")

        # ── 3. TAG_EPISODE_TITLE (0x22): Short title (number) ──
        encoder.write_string_field(VSMetaEncoder.TAG_EPISODE_TITLE, data.number, label="episodeTitle")

        # ── 4. TAG_YEAR (0x28): Year ──
        if data.year:
            try:
                year = int(data.year)
                if year > 0:
                    encoder.write_varint_field(VSMetaEncoder.TAG_YEAR, year, label="year")
            except ValueError:
                pass

        # ── 5. TAG_EPISODE_RELEASE_DATE (0x32): Release date ──
        if data.release:
            parsed = parse_release_date(data.release)
            if parsed:
                date_str = f"{parsed[0]:04d}-{parsed[1]:02d}-{parsed[2]:02d}"
                encoder.write_string_field(VSMetaEncoder.TAG_EPISODE_RELEASE_DATE, date_str, label="releaseDate")

        # ── 6. TAG_EPISODE_LOCKED (0x38): Lock metadata ──
        if manager.config.vsmeta_locked:
            encoder.write_varint_field(VSMetaEncoder.TAG_EPISODE_LOCKED, 1, label="locked")

        # ── 7. TAG_CHAPTER_SUMMARY (0x42): Plot / summary ──
        summary = data.outline or data.originalplot or ""
        encoder.write_string_field(VSMetaEncoder.TAG_CHAPTER_SUMMARY, summary, label="summary")

        # ── 8. TAG_EPISODE_META_JSON (0x4A): External IDs as JSON ──
        if data.external_ids:
            external_ids_clean = {str(k): v for k, v in data.external_ids.items() if v}
            if external_ids_clean:
                meta = {"com.synology.FileAssets": {}, "external_ids": external_ids_clean}
                encoder.write_string_field(
                    VSMetaEncoder.TAG_EPISODE_META_JSON,
                    json.dumps(meta, ensure_ascii=False),
                    label="episodeMetaJson",
                )

        # ── 9. TAG_GROUP1 (0x52): Cast / director / genre / writer ──

        def build_group1(sub):
            # Cast (actors)
            actor_list = data.all_actors if len(data.all_actors) > len(data.actors) else data.actors
            if actor_list:
                limit = manager.config.vsmeta_actor_limit
                for name in actor_list[:limit]:
                    sub.write_string_field(VSMetaEncoder.TAG1_CAST, name, label="cast")

            # Director
            if data.directors:
                for name in data.directors:
                    sub.write_string_field(VSMetaEncoder.TAG1_DIRECTOR, name, label="director")

            # Genre / tags (with mosaic prefix)
            tag_items = list(data.tags)
            if data.mosaic and data.mosaic not in tag_items:
                tag_items.insert(0, data.mosaic)
            if tag_items:
                limit = manager.config.vsmeta_tag_limit
                for t in tag_items[:limit]:
                    sub.write_string_field(VSMetaEncoder.TAG1_GENRE, t, label="genre")

            # Writer (reserved, no data source currently)

        encoder.write_submessage(VSMetaEncoder.TAG_GROUP1, build_group1, label="group1")

        # ── 10. TAG_CLASSIFICATION (0x5A): Content rating / mosaic ──
        if data.mosaic:
            encoder.write_string_field(VSMetaEncoder.TAG_CLASSIFICATION, data.mosaic, label="classification")

        # ── 11. TAG_RATING (0x60): Score ──
        encoder.write_rating(data.score, label="rating")

        # ── 12. TAG_EPISODE_THUMB (0x8A + 0x92): Poster image ──
        if manager.config.vsmeta_include_poster:
            encoder.write_poster(poster_path, label="poster")

        # ── 13. TAG_GROUP2 (0x9A + index 0x01): Series info + poster ──

        def build_group2(sub):
            # Season / episode (always 0 for movies)
            sub.write_varint_field(VSMetaEncoder.TAG2_SEASON, 0, label="season")
            sub.write_varint_field(VSMetaEncoder.TAG2_EPISODE, 0, label="episode")

            # TV show year
            if data.year:
                try:
                    sub.write_varint_field(VSMetaEncoder.TAG2_TV_SHOW_YEAR, int(data.year), label="tvshowYear")
                except ValueError:
                    pass

            # TV show release date
            if data.release:
                parsed = parse_release_date(data.release)
                if parsed:
                    date_str = f"{parsed[0]:04d}-{parsed[1]:02d}-{parsed[2]:02d}"
                    sub.write_string_field(VSMetaEncoder.TAG2_RELEASE_DATE_TV_SHOW, date_str, label="tvshowReleaseDate")

            # TV show locked
            if manager.config.vsmeta_locked:
                sub.write_varint_field(VSMetaEncoder.TAG2_LOCKED, 1, label="tvshowLocked")

            # TV show summary (series name)
            if data.series:
                sub.write_string_field(VSMetaEncoder.TAG2_TVSHOW_SUMMARY, data.series, label="tvshowSummary")

            # Poster image in GROUP2
            if manager.config.vsmeta_include_poster:
                sub.write_poster_in_group2(poster_path, label="poster_g2")

            # TV show meta JSON (default)
            sub.write_string_field(
                VSMetaEncoder.TAG2_TVSHOW_META_JSON, VSMetaEncoder.DEFAULT_META_JSON, label="tvshowMetaJson"
            )

        encoder.write_submessage(VSMetaEncoder.TAG_GROUP2, build_group2, label="group2", index=0x01)

        # ── 14. TAG_GROUP3 (0xAA + index 0x01): Backdrop + timestamp (movies) ──

        def build_group3(sub):
            # Backdrop image
            if manager.config.vsmeta_include_backdrop:
                sub.write_backdrop_in_group3(backdrop_path, label="backdrop")

            # Timestamp (current Unix seconds)
            sub.write_varint_field(VSMetaEncoder.TAG3_TIMESTAMP, int(time.time()), label="timestamp")

        encoder.write_submessage(VSMetaEncoder.TAG_GROUP3, build_group3, label="group3", index=0x01)

        # ── Write atomically (tmp → rename) ──
        tmp_file = vsmeta_file.with_suffix(".vsmeta.tmp")
        vsmeta_data = encoder.get_bytes()
        async with aiofiles.open(tmp_file, "wb") as f:
            await f.write(vsmeta_data)
        await move_file_async(tmp_file, vsmeta_file)

        LogBuffer.log().write(
            f"\n 🍀 VSMETA done! ({get_used_time(start_time)}s) [{len(vsmeta_data)}B] tags: {', '.join(encoder.written_tags)}"
        )
        return True

    except Exception as e:
        LogBuffer.log().write(f"\n 🔴 VSMETA failed! \n     {str(e)}")
        signal.show_traceback_log(traceback.format_exc())
        signal.show_log_text(traceback.format_exc())
        return False
