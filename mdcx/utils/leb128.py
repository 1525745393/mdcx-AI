"""LEB128 encoding/decoding utilities.

Used by VSMETA encoder (and potentially other binary formats).
"""


def encode_leb128(value: int) -> bytes:
    """Encode unsigned integer using LEB128 variable-length encoding."""
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


# Alias for protobuf varint wire type encoding (same as LEB128 unsigned)
encode_varint = encode_leb128


def decode_leb128(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Decode LEB128 encoded integer, returns (value, next_offset)."""
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
    """Encode string with LEB128 length prefix."""
    utf8 = s.encode("utf-8")
    return encode_leb128(len(utf8)) + utf8


def encode_boolean(value: bool) -> bytes:
    """Encode boolean as LEB128 integer (1 or 0)."""
    return encode_leb128(1 if value else 0)


def encode_int(value: int) -> bytes:
    """Encode integer using LEB128."""
    return encode_leb128(value)


def encode_date(year: int, month: int, day: int) -> bytes:
    """Encode date as 'YYYY-MM-DD' string with LEB128 prefix."""
    return encode_string(f"{year:04d}-{month:02d}-{day:02d}")
