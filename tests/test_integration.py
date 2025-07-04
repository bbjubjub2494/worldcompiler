from pathlib import Path

import boa

def test_compile_hex0(hex2_contract):
    build = Path("build")
    input_str = (build/"hex0.hex2").read_text()
    expected_output = (build/"hex0.bin").read_bytes()
    r = boa.env.raw_call(to_address=hex2_contract, data=input_str.encode())
    assert r.is_success
    assert r.output == expected_output
