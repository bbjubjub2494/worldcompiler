from .parser import ParserWithComments, ParserStrict, Tokenizer, TokenType

class Hex0Parser(ParserStrict, ParserWithComments):
    @classmethod
    def _tokenizer(cls) -> Tokenizer:
        return super()._tokenizer().add_token_type(
            TokenType(b'hex', rb'[0-9a-fA-F]{2}'),
        )

    def __init__(self) -> None:
        print(self.tokenizer.pattern)
        self.output = bytearray()

    def _handle_hex(self, value: bytes) -> None:
        self.output.append(int(value, 16))

    def _result(self) -> bytes:
        return bytes(self.output)
