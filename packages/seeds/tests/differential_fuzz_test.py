import pytest

import boa
from hypothesis import given, strategies as st

import ethbootstrap_seeds
from ethbootstrap_languages import Hex0Parser

@pytest.fixture(scope="module")
def hex0_contract():
    target = boa.env.generate_address()
    boa.env.set_code(target, ethbootstrap_seeds.hex0_bytecode)
    return target

@given(input_data=st.lists(st.from_regex(Hex0Parser.tokenizer.pattern, fullmatch=True)))
def test_hex0(hex0_contract, input_data):
    input_data = b''.join(input_data)
    expected_output = Hex0Parser.parse(input_data)
    r = boa.env.raw_call(to_address=hex0_contract, data=input_data)
    assert r.is_success
    assert r.output == expected_output
