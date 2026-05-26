
#!/usr/bin/env python3

from io import BytesIO
from mdcx.utils.leb128 import decode_leb128


def parse_vsmeta_file(path):
    with open(path, "rb") as f:
        data = f.read()
    stream = BytesIO(data)
    fields = []
    offset = 0
    while True:
        tag_byte = stream.read(1)
        if not tag_byte:
            break
        tag = tag_byte[0]
        field_entry = {"offset": offset, "tag": tag}
        offset += 1
        # Check if this tag has an index byte (as per VSMetaEncoder)
        if tag in [0x8a, 0x92, 0x9a, 0xaa]:
            index_byte = stream.read(1)
            field_entry["index"] = index_byte[0]
            offset +=1
        # Now read wire type
        wire_type = tag & 0x7
        if wire_type == 0:  # Varint
            # Read until we get the value
            val_bytes = b''
            while True:
                b = stream.read(1)
                val_bytes += b
                if not (b[0] & 0x80):
                    break
            field_entry["value_bytes"] = val_bytes
            offset += len(val_bytes)
        elif wire_type == 2:  # Length-delimited
            len_bytes = b''
            while True:
                b = stream.read(1)
                len_bytes += b
                if not (b[0] & 0x80):
                    break
            length, _ = decode_leb128(len_bytes, 0)
            field_entry["len_bytes"] = len_bytes
            field_entry["length"] = length
            payload = stream.read(length)
            field_entry["payload"] = payload
            offset += len(len_bytes) + length
        fields.append(field_entry)
    return fields


file1_fields = parse_vsmeta_file("/workspace/IPX-967.mp4.vsmeta")
file2_fields = parse_vsmeta_file("/workspace/打开翻译的无法识别IPX-967.mp4.vsmeta")


print("="*150)
print(f"{'File1 Offset':<15} {'File2 Offset':<15} {'Tag':<8} {'Index':<8} {'File1 Len':<10} {'File2 Len':<10} {'Diff':<10} {'File1 LenBytes':<20} {'File2 LenBytes':<20}")
print("="*150)
for f1, f2 in zip(file1_fields, file2_fields):
    len1 = f1.get('length', '-')
    len2 = f2.get('length', '-')
    len_bytes1 = f1.get('len_bytes', None)
    len_bytes2 = f2.get('len_bytes', None)
    diff = len2 - len1 if (isinstance(len1, int) and isinstance(len2, int)) else '-'
    print(
        f"{hex(f1['offset']):<15} {hex(f2['offset']):<15} {hex(f1['tag']):<8} "
        f"{hex(f1.get('index', 0)):<8} {str(len1):<10} {str(len2):<10} {str(diff):<10} "
        f"{str(len_bytes1):<20} {str(len_bytes2):<20}"
    )
print("\n\n")
print("=== Checking for any other differences (tag, index, len_bytes) ===")
for i, (f1, f2) in enumerate(zip(file1_fields, file2_fields)):
    if f1['tag'] != f2['tag']:
        print(f"Field {i}: Tag mismatch! File1={hex(f1['tag'])}, File2={hex(f2['tag'])}")
    if f1.get('index', 0) != f2.get('index', 0):
        print(f"Field {i}: Index mismatch! File1={hex(f1.get('index',0))}, File2={hex(f2.get('index',0))}")
    if f1.get('len_bytes', None) != f2.get('len_bytes', None):
        print(f"Field {i}: Len_bytes mismatch! File1={f1.get('len_bytes')}, File2={f2.get('len_bytes')}")
print("Check completed.")

