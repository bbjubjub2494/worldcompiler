import boa

def test_hex(hex0_contract):
    r = boa.env.raw_call(to_address=hex0_contract, data=b"ab # comment\n cd")
    assert r.is_success
    assert r.output == b"\xab\xcd"
