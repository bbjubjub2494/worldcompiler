import logging

import pytest
import eth_utils.logging
import eth.exceptions

import boa
import hypothesis
from hypothesis import given, strategies as st

import ethbootstrap_seeds
from ethbootstrap_languages import Hex0Parser, Hex2Parser


@pytest.fixture(scope="module")
def hex0_contract():
    target, _ = boa.env.deploy_code(
        bytecode=ethbootstrap_seeds.trivial_initcode_prefix
        + ethbootstrap_seeds.hex0_bytecode
    )
    return target


@pytest.fixture(scope="module")
def hex2_contract():
    target, _ = boa.env.deploy_code(
        bytecode=ethbootstrap_seeds.trivial_initcode_prefix
        + ethbootstrap_seeds.hex2_bytecode
    )
    return target


@pytest.fixture()
def debug2(caplog):
    eth_utils.logging.setup_DEBUG2_logging()
    caplog.set_level(logging.DEBUG2, logger="eth.vm.computation.BaseComputation")


def from_tokenizer(tokenizer):
    pattern = rb"(%s)*" % tokenizer.pattern.pattern
    return st.from_regex(pattern, fullmatch=True)


@given(input_data=from_tokenizer(Hex0Parser.tokenizer))
def test_hex0(hex0_contract, input_data):
    expected_output = Hex0Parser.parse(input_data)
    r = boa.env.raw_call(to_address=hex0_contract, data=input_data)
    assert r.is_success
    assert r.output == expected_output


@given(input_data=from_tokenizer(Hex2Parser.tokenizer))
def test_hex2(hex2_contract, input_data):
    expected_output = Hex2Parser.parse(input_data)
    r = boa.env.raw_call(to_address=hex2_contract, data=input_data)
    assert r.is_success
    assert r.output == expected_output


def test_dirty_transient_guard(hex2_contract):
    input_data = b"00" * 32
    r = boa.env.raw_call(to_address=hex2_contract, data=input_data)
    assert r.is_success
    with pytest.raises(eth.exceptions.Revert):
        r = boa.env.raw_call(to_address=hex2_contract, data=input_data)
