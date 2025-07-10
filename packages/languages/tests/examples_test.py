from typing import NamedTuple

import pytest

class Example(NamedTuple):
    input: bytes
    expected_output: bytes | None = None
    error: type[Exception] | None = None

    def check(self, parser):
        if self.error:
            with pytest.raises(self.error):
                parser.parse(self.input)
        elif self.expected_output is not None:
            assert parser.parse(self.input) == self.expected_output
        else:
            parser.parse(self.input)  # ensure it doesn't raise an error

from ethbootstrap_languages.parser import ParserWithWhitespace, ParserWithComments

from ethbootstrap_languages.parser import ParserStrict

STRICT_EXAMPLES = [
    Example(b"garb", error=ValueError),
]

def test_parser_examples():
    for example in STRICT_EXAMPLES:
        example.check(ParserStrict)

WHITESPACE_EXAMPLES = [
    Example(b" \t"),
]

COMMENT_EXAMPLES = WHITESPACE_EXAMPLES + [
    Example(b"; garb"),
]

def test_parser_examples():
    for example in WHITESPACE_EXAMPLES:
        example.check(ParserWithWhitespace)
    for example in COMMENT_EXAMPLES:
        example.check(ParserWithComments)

from ethbootstrap_languages import Hex0Parser

HEX0_EXAMPLES = COMMENT_EXAMPLES + [
    Example(b"01 02 03 04 ; comment\n05 06", b'\x01\x02\x03\x04\x05\x06'),
]
def test_hex0_examples():
    for example in HEX0_EXAMPLES:
        example.check(Hex0Parser)

from ethbootstrap_languages import Hex2Parser

HEX2_EXAMPLES = HEX0_EXAMPLES + [
    Example(b":label1 01 02 03 04 +label1", b'\x01\x02\x03\x04\x00'),
    Example(b"+label2 01 02 03 04 :label2", b'\x05\x01\x02\x03\x04'),
    Example(b"a1 +X b2 :X c3 +X d4", b'\xa1\x03\xb2\xc3\x03\xd4'),
]

def test_hex2_examples():
    for example in HEX2_EXAMPLES:
        example.check(Hex2Parser)
