import time
import traceback
from io import BytesIO
from pathlib import Path

import aiofiles
from PIL import Image

from ..config.enums import DownloadableFile, KeepableFile
from ..config.manager import manager
from ..config.resource_policy import resource_policy
from ..models.log_buffer import LogBuffer
from ..models.types import CrawlersResult, FileInfo
from ..signals import signal
from ..utils import get_used_time


def encode_leb128(value: int) -> bytes:
    """Encode integer using LEB128 encoding"""
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        result.append(byte)
        if not value:
            break
    return bytes(result)


def decode_leb128(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Decode LEB128 encoded integer"""
    result = 0
    shift = 0
    i = offset
    while i < len(data):
        byte = data[i]
        i += 1
        result |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return result, i


def encode_string(s: str) -> bytes:
    """Encode string with LEB128 length prefix"""
    utf8 = s.encode("utf-8")
    return encode_leb128(len(utf8)) + utf8


def encode_boolean(value: bool) -> bytes:
    """Encode boolean value"""
    return encode_leb128(1 if value else 0)


def encode_int(value: int) -> bytes:
    """Encode integer value using LEB128"""
    return encode_leb128(value)


def encode_date(year: int, month: int, day: int) -> bytes:
    """Encode date as string YYYY-MM-DD"""
    return encode_string(f"{year:04d}-{month:02d}-{day:02d}")


class VSMetaEncoder:
    """VSMETA file encoder for Synology Video Station"""

    # Magic header for VSMETA
    MAGIC_HEADER = b"vsmeta"

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
                    # Convert image to JPEG
                    img_buffer = BytesIO()
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(img_buffer, format="JPEG", quality=90)
                    img_data = img_buffer.getvalue()
                self.write_tag(tag, encode_leb128(len(img_data)) + img_data)
            except Exception:
                pass

    def get_bytes(self) -> bytes:
        """Get the final VSMETA bytes"""
        return self.buffer.getvalue()


def parse_release_date(release_str: str) -> tuple[int, int, int]:
    """Parse release date string (YYYY-MM-DD)"""
    try:
        if release_str and len(release_str) >= 10:
            year = int(release_str[0:4])
            month = int(release_str[5:7])
            day = int(release_str[8:10])
            return year, month, day
    except (ValueError, IndexError):
        pass
    return 2000, 1, 1


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

        # Build display title
        if data.title and data.number:
            display_title = f"[{data.number}] {data.title}"
        elif data.title:
            display_title = data.title
        elif data.number:
            display_title = data.number
        else:
            display_title = file_info.file_name

        encoder.write_string_tag(VSMetaEncoder.TAG_TITLE, display_title)

        # Write summary/plot
        summary = data.outline or data.originalplot or ""
        if summary:
            encoder.write_string_tag(VSMetaEncoder.TAG_SUMMARY, summary)

        # Write release date
        if data.release:
            year, month, day = parse_release_date(data.release)
            encoder.write_tag(VSMetaEncoder.TAG_RELEASE_DATE, encode_date(year, month, day))
            if data.year:
                try:
                    encoder.write_int_tag(VSMetaEncoder.TAG_RELEASE_DATE, int(data.year))
                except ValueError:
                    pass
        elif data.year:
            try:
                year = int(data.year)
                encoder.write_tag(VSMetaEncoder.TAG_RELEASE_DATE, encode_date(year, 1, 1))
            except ValueError:
                pass

        # Write tagline (use series or studio)
        tagline = data.series or data.studio or data.publisher or ""
        if tagline:
            encoder.write_string_tag(VSMetaEncoder.TAG_TAGLINE, tagline)

        # Write rating
        if data.score:
            try:
                score = float(data.score)
                encoder.write_int_tag(VSMetaEncoder.TAG_RATING, int(score * 10))
            except ValueError:
                pass

        # Write runtime (in minutes)
        if data.runtime:
            try:
                runtime_str = str(data.runtime).replace(" ", "").replace("min", "")
                runtime = int(float(runtime_str))
                encoder.write_int_tag(VSMetaEncoder.TAG_RUNTIME, runtime)
            except ValueError:
                pass

        # Write genres/tags
        if data.tags:
            genre_str = ", ".join(data.tags[:10])  # Limit to first 10 tags
            encoder.write_string_tag(VSMetaEncoder.TAG_GENRE, genre_str)

        # Write director
        if data.directors:
            director_str = ", ".join(data.directors)
            encoder.write_string_tag(VSMetaEncoder.TAG_DIRECTOR, director_str)

        # Write actors
        if data.actors:
            actor_str = ", ".join(data.actors[:20])  # Limit to first 20 actors
            encoder.write_string_tag(VSMetaEncoder.TAG_ACTOR, actor_str)

        # Write studio
        if data.studio:
            encoder.write_string_tag(VSMetaEncoder.TAG_STUDIO, data.studio)
        elif data.publisher:
            encoder.write_string_tag(VSMetaEncoder.TAG_STUDIO, data.publisher)

        # Write collection/series
        if data.series:
            encoder.write_string_tag(VSMetaEncoder.TAG_COLLECTION, data.series)

        # Write images
        encoder.write_image_tag(VSMetaEncoder.TAG_POSTER, poster_path)
        encoder.write_image_tag(VSMetaEncoder.TAG_BACKDROP, backdrop_path)

        # Write locked flag (locked = true means don't auto-update metadata)
        encoder.write_boolean_tag(VSMetaEncoder.TAG_LOCKED, True)

        # Save to file
        vsmeta_data = encoder.get_bytes()
        async with aiofiles.open(vsmeta_file, "wb") as f:
            await f.write(vsmeta_data)

        LogBuffer.log().write(f"\n 🍀 VSMETA done! ({get_used_time(start_time)}s)")
        return True

    except Exception as e:
        LogBuffer.log().write(f"\n 🔴 VSMETA failed! \n     {str(e)}")
        signal.show_traceback_log(traceback.format_exc())
        signal.show_log_text(traceback.format_exc())
        return False
