#!/usr/bin/env python3
from io import BytesIO


def decode_varint(buffer: BytesIO):
    result = 0
    shift = 0
    while True:
        byte = buffer.read(1)
        if not byte:
            return None
        byte = byte[0]
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return result
        shift += 7


def parse_single_field(buffer: BytesIO, depth=0):
    indent = "  " * depth
    pos = buffer.tell()
    tag_byte = buffer.read(1)
    if not tag_byte:
        return None
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
        21: 'GROUP3',
    }
    
    field_name = field_names.get(field_number, f'FIELD_{field_number}')
    
    info = {
        'pos': pos,
        'tag_byte': tag_byte,
        'field_number': field_number,
        'wire_type': wire_type,
        'field_name': field_name,
    }
    
    if wire_type == 0:
        value = decode_varint(buffer)
        info['value'] = value
    elif wire_type == 2:
        length = decode_varint(buffer)
        info['length'] = length
        if field_number in [17, 18, 19, 21]:
            index_byte = buffer.read(1)
            if index_byte == b'\x01':
                info['has_index_byte'] = True
                info['index_byte'] = 0x01
                payload = buffer.read(length)
            else:
                buffer.seek(-1, 1)
                payload = buffer.read(length)
        else:
            payload = buffer.read(length)
        
        info['payload'] = payload
        try:
            info['payload_text'] = payload.decode('utf-8', errors='replace')
        except:
            pass
    
    return info


def parse_vsmeta(file_path, max_fields=30):
    with open(file_path, 'rb') as f:
        data = f.read()
    buffer = BytesIO(data)
    
    print(f"\n{'='*70}")
    print(f"File: {file_path}")
    print(f"Total size: {len(data)} bytes")
    print(f"{'='*70}")
    
    header = buffer.read(2)
    print(f"\nHeader at offset 0x00: {header.hex()}")
    
    for i in range(max_fields):
        field = parse_single_field(buffer)
        if not field:
            break
        
        print(f"\nField #{i+1} at 0x{field['pos']:04x}")
        print(f"  Tag: 0x{field['tag_byte']:02x}")
        print(f"  Field: {field['field_name']}")
        
        if 'value' in field:
            print(f"  Value: {field['value']}")
        if 'length' in field:
            print(f"  Length: {field['length']}")
            if 'has_index_byte' in field:
                print(f"  Index byte: 0x01")
            if 'payload_text' in field and field['field_name'] not in ['EPISODE_THUMB_DATA']:
                txt = field['payload_text']
                if len(txt) > 80:
                    txt = txt[:77] + '...'
                print(f"  Payload: {repr(txt)}")
            elif 'payload' in field:
                print(f"  Payload (first 32 hex): {field['payload'][:32].hex()}")
        
        if field['field_name'] == 'GROUP3':
            break  # stop after group3
    
    print(f"\nCurrent offset: 0x{buffer.tell():04x}")
    return data


if __name__ == '__main__':
    file1 = '/workspace/IPX-967.mp4.vsmeta'
    file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'
    
    data1 = parse_vsmeta(file1)
    data2 = parse_vsmeta(file2)
