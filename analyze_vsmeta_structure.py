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


def parse_vsmeta(file_path: str) -> dict:
    """Parse VSMETA file structure and return a human-readable description"""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    buffer = BytesIO(data)
    structure = []
    total_size = len(data)
    
    def read_position():
        return buffer.tell()
    
    try:
        # Read header
        pos = read_position()
        header_byte1 = buffer.read(1)
        header_byte2 = buffer.read(1)
        structure.append({
            'type': 'header',
            'pos': pos,
            'bytes': header_byte1 + header_byte2,
            'desc': f'Content type: movie (0x08 0x01)'
        })
        
        # Parse fields
        while buffer.tell() < total_size:
            pos = read_position()
            tag_byte = buffer.read(1)
            if not tag_byte:
                break
            
            tag_byte = tag_byte[0]
            field_number = (tag_byte >> 3)
            wire_type = tag_byte & 0x07
            
            field_info = {
                'pos': pos,
                'tag_byte': tag_byte,
                'field_number': field_number,
                'wire_type': wire_type
            }
            
            wire_type_names = {0: 'varint', 2: 'length-delimited'}
            field_info['wire_type_name'] = wire_type_names.get(wire_type, f'unknown({wire_type})')
            
            # Field number to name mapping
            field_names = {
                1: 'CONTENT_TYPE',
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
            field_info['field_name'] = field_names.get(field_number, f'UNKNOWN({field_number})')
            
            if wire_type == 0:  # varint
                value = decode_varint(buffer)
                field_info['value'] = value
                field_info['desc'] = f'{field_info["field_name"]} = {value}'
                structure.append(field_info)
            
            elif wire_type == 2:  # length-delimited
                # Check for index byte (used in image fields and groups)
                pos_before_len = read_position()
                length = decode_varint(buffer)
                field_info['length_pos'] = pos_before_len
                field_info['length'] = length
                
                # Check if next byte is index byte (0x01 for images/groups)
                next_byte = buffer.read(1)
                has_index_byte = False
                if next_byte and next_byte[0] == 0x01:
                    # Peek further to see if this makes sense
                    remaining = total_size - buffer.tell()
                    if remaining >= length - 1:
                        has_index_byte = True
                        field_info['has_index_byte'] = True
                        field_info['index_byte'] = 0x01
                    else:
                        buffer.seek(-1, 1)  # go back, not an index byte
                else:
                    if next_byte:
                        buffer.seek(-1, 1)  # go back
                
                payload_pos = read_position()
                payload = buffer.read(length)
                field_info['payload_pos'] = payload_pos
                field_info['payload'] = payload
                
                # Try to decode as UTF-8
                try:
                    text = payload.decode('utf-8')
                    preview = text[:100] + ('...' if len(text) > 100 else '')
                    field_info['payload_text'] = preview
                    field_info['payload_type'] = 'text'
                except UnicodeDecodeError:
                    field_info['payload_type'] = 'binary'
                    field_info['payload_preview'] = payload[:32].hex()
                
                structure.append(field_info)
            
            else:
                # Unknown wire type, just read 1 byte to progress
                buffer.read(1)
                field_info['error'] = 'Unknown wire type'
                structure.append(field_info)
    
    except Exception as e:
        structure.append({'type': 'error', 'error': str(e)})
    
    return {
        'file_path': file_path,
        'file_size': total_size,
        'structure': structure
    }


def compare_structures(result1: dict, result2: dict):
    """Compare two parsed VSMETA structures"""
    print(f"\n{'='*80}")
    print(f"FILE 1: {result1['file_path']} ({result1['file_size']} bytes)")
    print(f"FILE 2: {result2['file_path']} ({result2['file_size']} bytes)")
    print(f"{'='*80}\n")
    
    struct1 = result1['structure']
    struct2 = result2['structure']
    
    max_fields = max(len(struct1), len(struct2))
    
    for i in range(max_fields):
        f1 = struct1[i] if i < len(struct1) else None
        f2 = struct2[i] if i < len(struct2) else None
        
        print(f"FIELD {i+1}:")
        
        if f1 and f2:
            # Compare both fields
            if f1.get('field_name') == f2.get('field_name'):
                print(f"  Type: {f1.get('field_name')}")
                print(f"  File1 pos: {f1.get('pos')}, File2 pos: {f2.get('pos')}")
                
                if 'length' in f1 and 'length' in f2:
                    if f1['length'] != f2['length']:
                        print(f"  ⚠️  LENGTH DIFFERENT: File1={f1['length']}, File2={f2['length']}")
                    else:
                        print(f"  Length: {f1['length']} bytes")
                
                if 'payload_text' in f1 and 'payload_text' in f2:
                    if f1['payload_text'] != f2['payload_text']:
                        print(f"  ⚠️  PAYLOAD DIFFERENT:")
                        print(f"    File1: {repr(f1['payload_text'][:150])}")
                        print(f"    File2: {repr(f2['payload_text'][:150])}")
                    else:
                        print(f"  Payload: {repr(f1['payload_text'][:100])}")
                
                elif 'value' in f1 and 'value' in f2:
                    if f1['value'] != f2['value']:
                        print(f"  ⚠️  VALUE DIFFERENT: File1={f1['value']}, File2={f2['value']}")
                    else:
                        print(f"  Value: {f1['value']}")
            else:
                print(f"  ⚠️  FIELD TYPE MISMATCH: File1={f1.get('field_name')}, File2={f2.get('field_name')}")
        
        elif f1:
            print(f"  Only in File1: {f1.get('field_name', 'unknown')}")
        elif f2:
            print(f"  Only in File2: {f2.get('field_name', 'unknown')}")
        
        print()


if __name__ == '__main__':
    file1 = '/workspace/IPX-967.mp4.vsmeta'
    file2 = '/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta'
    
    result1 = parse_vsmeta(file1)
    result2 = parse_vsmeta(file2)
    
    compare_structures(result1, result2)
