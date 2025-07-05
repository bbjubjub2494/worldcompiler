from pathlib import Path

import boa

def test_M1_compile_hex0(hex2_contract, M1_contract):
    build = Path("build")
    contracts = Path("contracts")

    input_bytes = (contracts/"evm_defs.M1").read_bytes() + (contracts/"hex0.M1").read_bytes()
    r = boa.env.raw_call(to_address=M1_contract, data=input_bytes)
    assert r.is_success

    input_bytes = r.output
    expected_output = (build/"hex0.bin").read_bytes()
    r = boa.env.raw_call(to_address=hex2_contract, data=input_bytes)
    assert r.is_success
    assert r.output == expected_output

def test_hex2_compile_hex0(hex2_contract, M1_contract):
    build = Path("build")

    input_bytes = (build/"hex0.hex2").read_bytes()
    expected_output = (build/"hex0.bin").read_bytes()
    r = boa.env.raw_call(to_address=hex2_contract, data=input_bytes)
    assert r.is_success
    assert r.output == expected_output
