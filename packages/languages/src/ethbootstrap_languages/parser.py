from typing import NamedTuple

import functools, re

class TokenType(NamedTuple):
    name: bytes
    pattern: bytes
    priority: int = 500

    assert priority in range(100, 1000), "Priority must be between 100 and 999"

class Tokenizer:
    '''Declarative tokenizer
    Based on https://docs.python.org/3/library/re.html#writing-a-tokenizer
    '''
    def __init__(self, token_types=[]):
        self.token_types = list(token_types)

    def tokenize(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @functools.cached_property
    def pattern(self):
        token_types = sorted(self.token_types, key=lambda t: t.priority)
        code = b'|'.join(b'(?P<%s>%s)' % spec[:2] for spec in token_types)
        return re.compile(code)

    def tokenize(self, input: bytes):
        for m in self.pattern.finditer(input):
            kind = m.lastgroup
            value = m.group(kind)
            yield kind, value

    def add_token_type(self, *spec):
        return Tokenizer([*spec, *self.token_types])

class ParserBase:
    @classmethod
    def _tokenizer(cls):
        return Tokenizer()

    def __init_subclass__(cls):
        cls.tokenizer = cls._tokenizer()

    @classmethod
    def parse(cls, input: bytes):
        parser = cls()
        for kind, value in cls.tokenizer.tokenize(input):
            handler = getattr(parser, f'_handle_{kind}')
            handler(value)
        return parser._result()

    def _result(self):
        return None

class ParserStrict(ParserBase):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            TokenType(b'garbage', rb'.+', priority=999)
        )

    def _handle_garbage(self, value: bytes):
        raise ValueError(f'Unexpected bytes: {value!r}')

class ParserWithWhitespace(ParserBase):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            TokenType(b'whitespace', rb'\s+'),
        )

    def _handle_whitespace(self, _: bytes):
        pass

class ParserWithComments(ParserWithWhitespace):
    @classmethod
    def _tokenizer(cls):
        return super()._tokenizer().add_token_type(
            TokenType(b'comment', rb'[#;][^\n]*\n?'),
        )

    def _handle_comment(self, _: bytes):
        pass
