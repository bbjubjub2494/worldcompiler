from .parser import ParserWithComments

class Hex0Parser(ParserWithComments):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            (b'hex', rb'[0-9a-fA-F]{2}'),
        )

    def __init__(self):
        print(self.tokenizer.pattern)
        self.output = bytearray()

    def _handle_hex(self, value: bytes):
        self.output.append(int(value, 16))

    def _result(self):
        return bytes(self.output)
