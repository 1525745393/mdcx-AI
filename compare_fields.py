#!/usr/bin/env python3

from io import BytesIO
from collections import namedtuple

Field = namedtuple('Field', ['offset', 'tag', 'has_index', 'index', 'length', 'wire_type'])


def decode_varint_from_stream(stream: BytesIO):
    result = 0
    shift = 0
    while True:
        byte = stream.read(1)[0]
        result |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return result


def parse_fields(filename: str):
    fields = []
    with open(filename, 'rb') as f:
        data = f.read()
    stream = BytesIO(data)
    while True:
        offset = stream.tell()
        tag_byte = stream.read(1)
        if not tag_byte:
            break
        tag = tag_byte[0]
        wire_type = tag & 0x7
        has_index = tag in [0x8a, 0x92, 0x9a, 0xaa]
        index = 0
        if has_index:
            index_b = stream.read(1)
            if index_b:
                index = index_b[0]
        
        length = 0
        if wire_type == 0:
            # varint, we need to consume but don't need length
            decode_varint_from_stream(stream)
        elif wire_type == 2:
            length = decode_varint_from_stream(stream)
            # Consume the payload
            stream.read(length)
        
        fields.append(Field(offset, tag, has_index, index, length, wire_type))
    return fields


fields1 = parse_fields("/workspace/IPX-967.mp4.vsmeta")
fields2 = parse_fields("/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta")

print(f"{'File1 Offset':<12} {'File2 Offset':<12} {'Tag':<6} {'Index':<6} {'File1 Len':<10} {'File2 Len':<10} {'Diff':<8}")
print("-"*80)

for f1, f2 in zip(fields1, fields2):
    diff_offset = f2.offset - f1.offset
    diff_len = f2.length - f1.length
    print(f"{hex(f1.offset):<12} {hex(f2.offset):<12} {hex(f1.tag):<6} {hex(f1.index):<6} {f1.length:<10} {f2.length:<10} {diff_len:<8}")
