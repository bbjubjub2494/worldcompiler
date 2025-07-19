import logging

import pytest
import eth_utils.logging

import boa
import hypothesis
from hypothesis import given, strategies as st

import ethbootstrap_seeds
from ethbootstrap_languages import Hex0Parser, Hex2Parser


@pytest.fixture(scope="module")
def hex0_contract():
    target = boa.env.generate_address()
    boa.env.set_code(target, ethbootstrap_seeds.hex0_bytecode)
    return target

@pytest.fixture(scope="module")
def hex2_contract():
    target = boa.env.generate_address()
    boa.env.set_code(target, ethbootstrap_seeds.hex2_bytecode)
    return target

@pytest.fixture()
def debug2(caplog):
    eth_utils.logging.setup_DEBUG2_logging()
    caplog.set_level(logging.DEBUG2, logger="eth.vm.computation.BaseComputation")

@given(input_data=st.lists(st.from_regex(Hex0Parser.tokenizer.pattern, fullmatch=True)))
def test_hex0(hex0_contract, input_data):
    input_data = b"".join(input_data)
    expected_output = Hex0Parser.parse(input_data)
    r = boa.env.raw_call(to_address=hex0_contract, data=input_data)
    assert r.is_success
    assert r.output == expected_output


@given(input_data=st.lists(st.from_regex(Hex2Parser.tokenizer.pattern, fullmatch=True)))
def test_hex2(hex2_contract, input_data):
    input_data = b"".join(input_data)
    expected_output = Hex2Parser.parse(input_data)
    r = boa.env.raw_call(to_address=hex2_contract, data=input_data)
    assert r.is_success
    assert r.output == expected_output
