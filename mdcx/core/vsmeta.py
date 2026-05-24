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
from ..utils.leb128 import (
    encode_boolean,
    encode_date,
    encode_int,
    encode_leb128,
    encode_string,
)


class VSMetaEncoder:
    """VSMETA file encoder for Synology Video Station"""

    # Magic header for VSMETA
    MAGIC_HEADER = b"vsmeta"

    # Max image dimension for VSMETA (VS only needs thumbnail quality)
    MAX_IMAGE_DIMENSION = 1920

    # Tags for metadata fields
    TAG_TITLE = 0x01
    TAG_SUMMARY = 0x02
    TAG_RELEASE_DATE = 0x03
    TAG_TAGLINE = 0x04
    TAG_RATING = 0x05
    TAG_RUNTIME = 0x06
    TAG_GENRE = 0x07
    TAG_DIRECTOR = 0x08
    TAG_ACTOR = 0x09
    TAG_WRITER = 0x0A
    TAG_POSTER = 0x0B
    TAG_BACKDROP = 0x0C
    TAG_COLLECTION = 0x0D
    TAG_STUDIO = 0x0E
    TAG_LOCKED = 0x0F
    TAG_VERSION = 0x14  # VSMETA version

    def __init__(self):
        self.buffer = BytesIO()

    def write_header(self, version: int = 1):
        """Write VSMETA header"""
        self.buffer.write(self.MAGIC_HEADER)
        self.buffer.write(encode_leb128(version))

    def write_tag(self, tag: int, value: bytes):
        """Write a tag with its value"""
        self.buffer.write(encode_leb128(tag))
        self.buffer.write(encode_leb128(len(value)))
        self.buffer.write(value)

    def write_string_tag(self, tag: int, value: str):
        """Write a string tag"""
        if value:
            self.write_tag(tag, encode_string(value))

    def write_int_tag(self, tag: int, value: int):
        """Write an integer tag"""
        self.write_tag(tag, encode_int(value))

    def write_boolean_tag(self, tag: int, value: bool):
        """Write a boolean tag"""
        self.write_tag(tag, encode_boolean(value))

    def write_image_tag(self, tag: int, image_path: Path | None):
        """Write an image tag from file path"""
        if image_path and image_path.exists():
            try:
                with Image.open(image_path) as img:
                    # Resize if image exceeds max dimension
                    if max(img.size) > self.MAX_IMAGE_DIMENSION:
                        ratio = self.MAX_IMAGE_DIMENSION / max(img.size)
                        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                        img = img.resize(new_size, Image.LANCZOS)

                    # Convert image to JPEG
                    img_buffer = BytesIO()
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(img_buffer, format="JPEG", quality=90)
                    img_data = img_buffer.getvalue()
                self.write_tag(tag, encode_leb128(len(img_data)) + img_data)
            except Exception:
                LogBuffer.log().write(f"\n ⚠️ VSMETA image tag failed: {image_path}")
                signal.show_traceback_log(traceback.format_exc())

    def get_bytes(self) -> bytes:
        """Get the final VSMETA bytes"""
        return self.buffer.getvalue()


def parse_release_date(release_str: str) -> tuple[int, int, int] | None:
    """Parse release date string (YYYY-MM-DD), returns None if unparseable"""
    try:
        if release_str and len(release_str) >= 10:
            year = int(release_str[0:4])
            month = int(release_str[5:7])
            day = int(release_str[8:10])
            return year, month, day
    except (ValueError, IndexError):
        pass
    return None


def parse_score(score: str) -> int | None:
    """Parse score string to VSMETA rating (0-100), returns None if unparseable"""
    try:
        raw = str(score).strip()
        if not raw or raw.upper() in ("N/A", "NA", "NULL", "NONE", "-"):
            return None
        value = float(raw)
        if value < 0 or value > 10:
            return None
        return int(value * 10)
    except (ValueError, TypeError):
        return None


def parse_runtime(runtime: str) -> int | None:
    """Parse runtime string to minutes, returns None if unparseable

    Handles: '120', '120min', '120分钟', '2h', '1h30m', '90 mins', etc.
    """
    import re

    try:
        raw = str(runtime).strip()
        if not raw:
            return None

        # Pattern: "2h30m" or "1h"
        h_m_match = re.match(r"(\d+)\s*h\s*(\d+)\s*m", raw, re.IGNORECASE)
        if h_m_match:
            return int(h_m_match.group(1)) * 60 + int(h_m_match.group(2))

        # Pattern: "2h"
        h_match = re.match(r"(\d+)\s*h", raw, re.IGNORECASE)
        if h_match:
            return int(h_match.group(1)) * 60

        # Pattern: "120min" / "120分钟" / "90 mins"
        cleaned = re.sub(r"(分钟|mins?|minute)", "", raw, flags=re.IGNORECASE)
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
    Extracted from Scraper.process_one_file to improve testability.
    """
    # Mode 2 + "删除本地已下载的文件": never write vsmeta
    if main_mode == 2 and Switch.SORT_DEL in switch_on:
        return False

    # Modes 1/2/3, or mode 4 with "无NFO时刮削"
    if main_mode in [1, 2, 3] or (main_mode == 4 and not is_nfo_existed and ReadMode.NO_NFO_SCRAPE in read_mode):
        if DownloadableFile.VSMETA not in download_files:
            return False
        if KeepableFile.VSMETA in keep_files and is_nfo_existed:
            return False
        return True

    # Mode 4 (read-only): only write vsmeta when explicitly updating NFO
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
    """
    Generate and write VSMETA file for Synology Video Station

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
                from ..utils.file import delete_file_async

                await delete_file_async(vsmeta_file)
            return True
        LogBuffer.log().write(f"\n 🍀 VSMETA done! (old)({get_used_time(start_time)}s)")
        return True

    try:
        if not await aiofiles.os.path.exists(output_dir):
            await aiofiles.os.makedirs(output_dir)

        from ..utils.file import delete_file_async

        await delete_file_async(vsmeta_file)

        encoder = VSMetaEncoder()
        encoder.write_header(version=1)
        written_tags: list[str] = []

        # Build display title
        if data.title and data.number:
            display_title = f"[{data.number}] {data.title}"
        elif data.title:
            display_title = data.title
        elif data.number:
            display_title = data.number
        else:
            display_title = file_info.file_name

        # Append original title if different from display title
        if data.originaltitle and data.originaltitle != data.title:
            display_title += f" ({data.originaltitle})"

        encoder.write_string_tag(VSMetaEncoder.TAG_TITLE, display_title)
        written_tags.append("title")

        # Write summary/plot
        summary = data.outline or data.originalplot or ""
        if summary:
            encoder.write_string_tag(VSMetaEncoder.TAG_SUMMARY, summary)
            written_tags.append("summary")

        # Write release date
        if data.release:
            parsed = parse_release_date(data.release)
            if parsed:
                encoder.write_tag(VSMetaEncoder.TAG_RELEASE_DATE, encode_date(*parsed))
                written_tags.append("release_date")
        elif data.year:
            try:
                year = int(data.year)
                encoder.write_tag(VSMetaEncoder.TAG_RELEASE_DATE, encode_date(year, 1, 1))
                written_tags.append("release_date(year)")
            except ValueError:
                pass

        # Write tagline (use series or studio)
        tagline = data.series or data.studio or data.publisher or ""
        if tagline:
            encoder.write_string_tag(VSMetaEncoder.TAG_TAGLINE, tagline)
            written_tags.append("tagline")

        # Write rating
        rating = parse_score(data.score)
        if rating is not None:
            encoder.write_int_tag(VSMetaEncoder.TAG_RATING, rating)
            written_tags.append("rating")

        # Write runtime (in minutes)
        runtime = parse_runtime(data.runtime)
        if runtime is not None:
            encoder.write_int_tag(VSMetaEncoder.TAG_RUNTIME, runtime)
            written_tags.append("runtime")

        # Write genres/tags
        if data.tags:
            genre_str = ", ".join(data.tags[:10])  # Limit to first 10 tags
            encoder.write_string_tag(VSMetaEncoder.TAG_GENRE, genre_str)
            written_tags.append("genre")

        # Write director
        if data.directors:
            director_str = ", ".join(data.directors)
            encoder.write_string_tag(VSMetaEncoder.TAG_DIRECTOR, director_str)
            written_tags.append("director")

        # Write actors (prefer all_actors for completeness)
        actor_list = data.all_actors if len(data.all_actors) > len(data.actors) else data.actors
        if actor_list:
            actor_str = ", ".join(actor_list[:20])  # Limit to first 20 actors
            encoder.write_string_tag(VSMetaEncoder.TAG_ACTOR, actor_str)
            written_tags.append("actor")

        # Write studio
        if data.studio:
            encoder.write_string_tag(VSMetaEncoder.TAG_STUDIO, data.studio)
            written_tags.append("studio")
        elif data.publisher:
            encoder.write_string_tag(VSMetaEncoder.TAG_STUDIO, data.publisher)
            written_tags.append("studio(publisher)")

        # Write collection/series
        if data.series:
            encoder.write_string_tag(VSMetaEncoder.TAG_COLLECTION, data.series)
            written_tags.append("collection")

        # Write images
        encoder.write_image_tag(VSMetaEncoder.TAG_POSTER, poster_path)
        if poster_path and poster_path.exists():
            written_tags.append("poster")
        encoder.write_image_tag(VSMetaEncoder.TAG_BACKDROP, backdrop_path)
        if backdrop_path and backdrop_path.exists():
            written_tags.append("backdrop")

        # Write locked flag (locked = true means don't auto-update metadata)
        encoder.write_boolean_tag(VSMetaEncoder.TAG_LOCKED, True)
        written_tags.append("locked")

        # Save to file
        vsmeta_data = encoder.get_bytes()
        async with aiofiles.open(vsmeta_file, "wb") as f:
            await f.write(vsmeta_data)

        LogBuffer.log().write(
            f"\n 🍀 VSMETA done! ({get_used_time(start_time)}s) [{len(vsmeta_data)}B] tags: {', '.join(written_tags)}"
        )
        return True

    except Exception as e:
        LogBuffer.log().write(f"\n 🔴 VSMETA failed! \n     {str(e)}")
        signal.show_traceback_log(traceback.format_exc())
        signal.show_log_text(traceback.format_exc())
        return False
