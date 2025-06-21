import boa
from boa.util.abi import Address, abi_decode

def test_increment(hex0_contract):
    r = boa.env.raw_call(to_address=hex0_contract, data=b"ab # comment\n cd")
    assert r.is_success
    deployed_address = abi_decode("address", r.output)
    assert boa.env.get_code(deployed_address) == b"\xab\xcd"
