import boa
from vyper.utils import keccak256

# FIXME duplicated
HEX0_TESTCASES = [
    (b"", b""),
    (b"00", b"\x00"),
    (b"10", b"\x10"),
    (b"98", b"\x98"),
    (b" AB", b"\xab"),
    (b"xAB", b"\xab"),
    (b"ab # comment\n cd", b"\xab\xcd"),
    (b"ABCD", b"\xab\xcd"),
    (b"AB CD EF # comment", b"\xab\xcd\xef"),
]

def test_input_addressed_registry(hex0_contract, inputaddressed_registry):
    for input_bytes, expected_output in HEX0_TESTCASES:
        inputaddressed_registry.register(hex0_contract, input_bytes)

    for input_bytes, expected_output in HEX0_TESTCASES:
        codehash = keccak256(boa.env.get_code(hex0_contract))
        output = inputaddressed_registry.get(codehash, keccak256(input_bytes))
        assert output == keccak256(expected_output), f"Failed for input: {input_bytes.hex()}"
