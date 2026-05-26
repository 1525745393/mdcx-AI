#!/usr/bin/env python3
import struct
from io import BytesIO


def decode_varint(buffer: BytesIO) -> int:
    """Decode LEB128 varint from buffer"""
    result = 0
    shift = 0
    while True:
        byte = buffer.read(1)[0]
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return result
        shift += 7


def parse_vsmeta_header(file_path: str, max_fields=20):
    """Parse VSMETA file header and first few fields"""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    buffer = BytesIO(data)
    structure = []
    total_size = len(data)
    
    print(f"\n{'='*80}")
    print(f"File: {file_path}")
    print(f"Size: {total_size} bytes")
    print(f"{'='*80}")
    
    # Read header
    header = buffer.read(2)
    print(f"\nHeader: {header.hex()} (should be 08 01 for movie)")
    
    field_count = 0
    while buffer.tell() < total_size and field_count < max_fields:
        pos = buffer.tell()
        tag_byte = buffer.read(1)
        if not tag_byte:
            break
        
        tag_byte = tag_byte[0]
        field_number = (tag_byte >> 3)
        wire_type = tag_byte & 0x07
        
        # Field names
        field_names = {
            2: 'SHOW_TITLE',
            3: 'SHOW_TITLE2',
            4: 'EPISODE_TITLE',
            5: 'YEAR',
            6: 'EPISODE_RELEASE_DATE',
            7: 'EPISODE_LOCKED',
            8: 'CHAPTER_SUMMARY',
            9: 'EPISODE_META_JSON',
            10: 'GROUP1',
            11: 'CLASSIFICATION',
            12: 'RATING',
            17: 'EPISODE_THUMB_DATA',
            18: 'EPISODE_THUMB_MD5',
            19: 'GROUP2',
            21: 'GROUP3'
        }
        field_name = field_names.get(field_number, f'FIELD_{field_number}')
        
        wire_name = {0: 'VARINT', 2: 'LENGTH_DELIMITED'}.get(wire_type, f'WIRE_{wire_type}')
        
        print(f"\nField {field_count+1}:")
        print(f"  Position: {pos}")
        print(f"  Tag byte: 0x{tag_byte:02x}")
        print(f"  Field: {field_name} (wire: {wire_name})")
        
        if wire_type == 0:  # varint
            value = decode_varint(buffer)
            print(f"  Value: {value}")
        elif wire_type == 2:  # length-delimited
            length = decode_varint(buffer)
            print(f"  Length: {length} bytes")
            
            payload = buffer.read(length)
            try:
                text = payload.decode('utf-8')
                if len(text) > 200:
                    text = text[:200] + '...'
                print(f"  Text: {repr(text)}")
            except UnicodeDecodeError:
                print(f"  Data (first 32 bytes): {payload[:32].hex()}")
        
        field_count += 1
        
        # Stop if we hit the image data (which is large)
        if field_number == 17 and length > 1000:  # EPISODE_THUMB_DATA
            print("\n[Reached image data, stopping analysis here]")
            break
    
    print()


if __name__ == '__main__':
    file1 = '/workspace/IPX-967.mp4.vsmeta'
    file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'
    
    parse_vsmeta_header(file1)
    parse_vsmeta_header(file2)
