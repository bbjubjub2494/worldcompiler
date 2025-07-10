from typing import NamedTuple

from .parser import ParserWithComments, ParserStrict, TokenType

class LabelReference(NamedTuple):
    label: bytes
    length: int

class Hex2Parser(ParserStrict, ParserWithComments):
    @classmethod
    def _tokenizer(cls):
        label = rb"([a-zA-Z_][a-zA-Z0-9_]*)"
        return super()._tokenizer().add_token_type(
            TokenType(b'label_definition', rb':'+label),
            TokenType(b'label_reference', rb'\+'+label),
            TokenType(b'hex', rb'[0-9a-fA-F]{2}'),
        )

    def __init__(self):
        super().__init__()
        self.offsets = {}
        self.chunks_or_references = [bytearray()]
        self.current_offset = 0

    def _handle_label_definition(self, value: bytes):
        label = value[1:]
        self.offsets[label] = self.current_offset

    def _handle_label_reference(self, value: bytes):
        label = value[1:]
        lr = LabelReference(label, 1)
        self.chunks_or_references.append(lr)
        self.current_offset += lr.length
        self.chunks_or_references.append(bytearray())

    def _handle_hex(self, value: bytes):
        self.chunks_or_references[-1].append(int(value, 16))
        self.current_offset += 1

    def _result(self):
        output = bytearray()
        for chunk in self.chunks_or_references:
            if isinstance(chunk, LabelReference):
                label = chunk.label
                if label not in self.offsets:
                    raise ValueError(f'Undefined label: {label.decode("ascii")}')
                output.extend(self.offsets[label].to_bytes(1, 'big'))
            else:
                output.extend(chunk)
        return bytes(output)
