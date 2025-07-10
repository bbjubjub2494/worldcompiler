import itertools, re

COMMENT = re.compile(rb'[#;][^\n]*\n?')

def strip_comments(chunk: bytes):
    yield from re.split(COMMENT, chunk)

HEX = re.compile(rb'[0-9a-fA-F]{2}')
def decode_hex(chunk: bytes):
    return bytes(int(byte.decode('ascii'), 16) for byte in re.findall(HEX, chunk))

LABEL = re.compile(rb':([a-zA-Z_][a-zA-Z0-9_]*)')
POINTER = re.compile(rb'\+([a-zA-Z_][a-zA-Z0-9_]*)')
def decode_hex_with_labels(chunks):
    cur_offset = 0
    offsets = {}
    chunks_or_pointers = []
    breakpoint()
    for chunk in chunks:
        for _ in itertools.batched(LABEL.split(chunk), n=2):
            try:
                chunk, label = _
            except ValueError:
                chunk = _[0]
                label = None
            for _ in itertools.batched(POINTER.split(chunk), n=2):
                try:
                    chunk, pointer = _
                except ValueError:
                    chunk = _[0]
                    pointer = None
                chunk = decode_hex(chunk)
                chunks_or_pointers.append(chunk)
                cur_offset += len(chunk)
                if pointer:
                    chunks_or_pointers.append(pointer)
                    cur_offset += 1 # 1-byte pointer
            if label:
                offsets[label] = cur_offset

    for _ in chunks_or_pointers:
        if isinstance(_, bytes):
            pointer = _
            if pointer in offsets:
                yield offsets[pointer].to_bytes(1, 'big')
        else:
            yield _

print(list(strip_comments(b"hello # world\nthis is a test; comment")))

print(decode_hex(b"hello 0a 1b 2c 3d 4e"))
print(list(decode_hex_with_labels([b"hello 0a 1b 2c 3d 4e:label1 +label2"])))
