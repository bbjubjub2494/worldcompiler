import functools, itertools, re

class Tokenizer:
    '''Declarative tokenizer
    Based on https://docs.python.org/3/library/re.html#writing-a-tokenizer
    '''
    def __init__(self, token_spec):
        self.token_spec = list(token_spec)

    def tokenize(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @functools.cached_property
    def pattern(self):
        code = b'|'.join(b'(?P<%s>%s)' % spec for spec in self.token_spec)
        return re.compile(code)

    def tokenize(self, input: bytes):
        for m in self.pattern.finditer(input):
            kind = m.lastgroup
            value = m.group(kind)
            yield kind, value

    def add_token_type(self, *spec):
        return Tokenizer([*spec, *self.token_spec])

class ParserBase:
    @classmethod
    def _tokenizer(cls):
        return Tokenizer([(b'garbage', rb'.+')])

    def __init_subclass__(cls):
        cls.tokenizer = cls._tokenizer()

    @classmethod
    def parse(cls, input: bytes):
        parser = cls()
        for kind, value in cls.tokenizer.tokenize(input):
            handler = getattr(parser, f'_handle_{kind}')
            handler(value)
        return parser._result()

    def _handle_garbage(self, value: bytes):
        raise ValueError(f'Unexpected bytes: {value!r}')

    def _result(self):
        return None

class ParserWithWhitespace(ParserBase):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            (b'whitespace', rb'\s+'),
        )

    def _handle_whitespace(self, _: bytes):
        pass

class ParserWithComments(ParserWithWhitespace):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            (b'comment', rb'[#;][^\n]*\n?'),
        )

    def _handle_comment(self, _: bytes):
        pass

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

print(ParserWithWhitespace.parse(b" \t"))
#print(ParserBase.parse(b"garb"))
print(ParserWithComments.parse(b"; garb"))
print(Hex0Parser.parse(b"01 02 03 04 ; comment\n05 06"))
