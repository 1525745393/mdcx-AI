#!/usr/bin/env python3

from io import BytesIO
import sys
import struct

# Copy of VSMetaEncoder tags for reference
class VSMetaDecoder:
    HEADER_MOVIE = b"\x08\x01"
    TAG_SHOW_TITLE = 0x12  # field 2, wire 2
    TAG_SHOW_TITLE2 = 0x1A  # field3
    TAG_EPISODE_TITLE = 0x22
    TAG_YEAR = 0x28
    TAG_EPISODE_RELEASE_DATE = 0x32
    TAG_EPISODE_LOCKED = 0x38
    TAG_CHAPTER_SUMMARY = 0x42
    TAG_EPISODE_META_JSON = 0x4A
    TAG_GROUP1 = 0x52
    TAG_CLASSIFICATION = 0x5A
    TAG_RATING = 0x60
    TAG_EPISODE_THUMB_DATA = 0x8A
    TAG_EPISODE_THUMB_MD5 = 0x92
    TAG_GROUP2 = 0x9A
    TAG_GROUP3 = 0xAA

    @staticmethod
    def decode_varint(data: BytesIO):
        """Decode a protobuf varint from BytesIO"""
        result = 0
        shift = 0
        while True:
            byte = data.read(1)[0]
            result |= (byte & 0x7F) << shift
            shift +=7
            if not (byte & 0x80):
                break
        return result

    def __init__(self, filename: str):
        self.filename = filename
        with open(filename, 'rb') as f:
            self.data = f.read()
        self.stream = BytesIO(self.data)

    def parse(self):
        print(f"\n--- Parsing {self.filename} ---")
        while True:
            pos = self.stream.tell()
            tag_byte = self.stream.read(1)
            if not tag_byte:
                break
            tag = tag_byte[0]

            wire_type = tag & 0x7
            field_number = tag >> 3

            # Check if this is an indexed field (like 0x8a, 0x92, 0x9a, 0xaa)
            has_index = False
            index = 0
            if tag in [0x8a, 0x92, 0x9a, 0xaa]:
                index_byte = self.stream.read(1)
                if index_byte:
                    index = index_byte[0]
                    has_index = True

            # Decode payload
            if wire_type == 0:  # varint
                value = self.decode_varint(self.stream)
                print(f"0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type}) index=0x{index:02x}  value={value}")
            elif wire_type == 2:  # length-delimited
                length = self.decode_varint(self.stream)
                payload = self.stream.read(length)
                try:
                    str_val = payload.decode('utf-8', errors='replace')
                    if len(str_val) > 100:
                        str_val = str_val[:100] + "..."
                    print(f"0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type}) index=0x{index:02x}  len={len(payload)}  data={repr(str_val)}")
                except:
                    print(f"0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type}) index=0x{index:02x}  len={len(payload)}")

                # Recursively parse GROUPs
                if tag in [0x52, 0x9a, 0xaa]:
                    sub_stream = BytesIO(payload)
                    self._parse_submessage(sub_stream, level=1)

    def _parse_submessage(self, sub_stream: BytesIO, level: int):
        indent = "  " * level
        while True:
            pos = sub_stream.tell()
            tag_byte = sub_stream.read(1)
            if not tag_byte:
                break
            tag = tag_byte[0]
            wire_type = tag &0x7
            field_number = tag >>3

            if wire_type ==0:
                value = self.decode_varint(sub_stream)
                print(f"{indent}0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type})  value={value}")
            elif wire_type ==2:
                length = self.decode_varint(sub_stream)
                payload = sub_stream.read(length)
                try:
                    str_val = payload.decode('utf-8', errors='replace')
                    if len(str_val) > 100:
                        str_val = str_val[:100] + "..."
                    print(f"{indent}0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type})  len={len(payload)}  data={repr(str_val)}")
                except:
                    print(f"{indent}0x{pos:06x}  tag=0x{tag:02x} (field {field_number}, wire {wire_type})  len={len(payload)}")


if __name__ == "__main__":
    decoder1 = VSMetaDecoder("/workspace/IPX-967.mp4.vsmeta")
    decoder1.parse()
    
    decoder2 = VSMetaDecoder("/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta")
    decoder2.parse()
