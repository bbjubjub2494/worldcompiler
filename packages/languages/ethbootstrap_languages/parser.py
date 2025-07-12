from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Generic, Iterator, NamedTuple, TypeVar

import functools, re


class TokenType(NamedTuple):
    name: bytes
    pattern: bytes
    priority: int = 500


class Tokenizer:
    """Declarative tokenizer
    Based on https://docs.python.org/3/library/re.html#writing-a-tokenizer
    """

    def __init__(self, token_types=[]):
        self.token_types = list(token_types)

    @functools.cached_property
    def pattern(self) -> re.Pattern:
        token_types = sorted(self.token_types, key=lambda t: t.priority)
        code = b"|".join(b"(?P<%s>%s)" % spec[:2] for spec in token_types)
        return re.compile(code)

    def tokenize(self, input) -> Iterator[tuple[str, bytes]]:
        for m in self.pattern.finditer(input):
            kind = m.lastgroup
            assert (
                kind is not None
            ), "this should never happen by construction of the pattern"
            value = m.group(kind)
            yield kind, value

    def add_token_type(self, *spec: TokenType) -> Tokenizer:
        return Tokenizer([*spec, *self.token_types])


R = TypeVar("R", covariant=True)


class Parser(Generic[R]):
    tokenizer: ClassVar[Tokenizer]

    @classmethod
    def _tokenizer(cls) -> Tokenizer:
        return Tokenizer()

    def __init_subclass__(cls) -> None:
        cls.tokenizer = cls._tokenizer()

    @classmethod
    def parse(cls, input: bytes) -> R:
        parser = cls()
        for kind, value in cls.tokenizer.tokenize(input):
            handler = getattr(parser, "_handle_" + kind)
            handler(value)
        return parser._result()

    @abstractmethod
    def _result(self) -> R: ...


class ParserBase(Parser[None]):
    def _result(self) -> None:
        return None


class ParserStrict(Parser):
    @classmethod
    def _tokenizer(cls):
        return (
            super()
            ._tokenizer()
            .add_token_type(TokenType(b"garbage", rb".+", priority=999))
        )

    def _handle_garbage(self, value: bytes):
        raise ValueError(f"Unexpected bytes: {value!r}")


class ParserWithWhitespace(Parser):
    @classmethod
    def _tokenizer(cls):
        return (
            super()
            ._tokenizer()
            .add_token_type(
                TokenType(b"whitespace", rb"\s+"),
            )
        )

    def _handle_whitespace(self, _: bytes):
        pass


class ParserWithComments(ParserWithWhitespace):
    @classmethod
    def _tokenizer(cls):
        return (
            super()
            ._tokenizer()
            .add_token_type(
                TokenType(b"comment", rb"[#;][^\n]*\n?"),
            )
        )

    def _handle_comment(self, _: bytes):
        pass
