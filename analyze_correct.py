#!/usr/bin/env python3
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


def parse_vsmeta_correct(file_path: str):
    """Parse VSMETA with correct handling of index bytes"""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    buffer = BytesIO(data)
    total_size = len(data)
    
    print(f"\n{'='*80}")
    print(f"File: {file_path}")
    print(f"Size: {total_size} bytes")
    print(f"{'='*80}")
    
    # Read header
    header = buffer.read(2)
    print(f"\nHeader: {header.hex()}")
    
    field_count = 0
    while buffer.tell() < total_size:
        pos = buffer.tell()
        tag_byte = buffer.read(1)
        if not tag_byte:
            break
        
        tag_byte = tag_byte[0]
        field_number = (tag_byte >> 3)
        wire_type = tag_byte & 0x07
        
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
        
        print(f"\nField {field_count+1}: {field_name} (pos={pos}, tag=0x{tag_byte:02x})")
        
        if wire_type == 0:  # varint
            value = decode_varint(buffer)
            print(f"  Value: {value}")
        elif wire_type == 2:  # length-delimited
            length = decode_varint(buffer)
            
            # Check if this field has an index byte
            # Fields 17, 18, 19, 21 should have index byte 0x01
            has_index = False
            if field_number in [17, 18, 19, 21]:
                # Peek at next byte
                peek_pos = buffer.tell()
                index_byte = buffer.read(1)
                if index_byte and index_byte[0] == 0x01:
                    has_index = True
                    print(f"  Index: 0x{index_byte[0]:02x}")
                    # Read actual length (length is total including index?)
                    # No, wait - index is separate, length is for payload only
                    payload = buffer.read(length)
                else:
                    buffer.seek(peek_pos)
                    payload = buffer.read(length)
            else:
                payload = buffer.read(length)
            
            print(f"  Length: {length} bytes (payload read: {len(payload)})")
            
            # Try to decode
            try:
                text = payload.decode('utf-8')
                if len(text) > 150:
                    text = text[:150] + '...'
                print(f"  Text: {repr(text)}")
            except UnicodeDecodeError:
                if len(payload) > 0:
                    print(f"  Data: starts with {payload[:32].hex()}")
                # Check if it looks like a sub-message
                if field_number in [10, 19, 21]:
                    print(f"  [This is a GROUP field, contains nested fields]")
        
        field_count += 1
        
        # Stop after group3
        if field_number == 21:
            break
    
    print()


if __name__ == '__main__':
    file1 = '/workspace/IPX-967.mp4.vsmeta'
    file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'
    
    parse_vsmeta_correct(file1)
    parse_vsmeta_correct(file2)
