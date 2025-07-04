import boa

HEX0_TESTCASES = [
    ("", b""),
    ("00", b"\x00"),
    ("10", b"\x10"),
    ("98", b"\x98"),
    (" AB", b"\xab"),
    ("xAB", b"\xab"),
    ("ab # comment\n cd", b"\xab\xcd"),
    ("ABCD", b"\xab\xcd"),
    ("AB CD EF # comment", b"\xab\xcd\xef"),
]

HEX2_TESTCASES = HEX0_TESTCASES + [
    (":label 00", b"\x00"),
    ("a :label b", b"\xab"), # note: maybe this should not work since the label is not aligned
    ("cdef :something", b"\xcd\xef"),
    (":a ab +a", b"\xab\x00"),
    ("ab :label +label", b"\xab\x01"),
    ("ab +label :label", b"\xab\x02"),
]

def test_hex0(hex0_contract):
    for input_str, expected_output in HEX0_TESTCASES:
        gas_pre = boa.env.get_gas_used()
        r = boa.env.raw_call(to_address=hex0_contract, data=input_str.encode())
        gas_post = boa.env.get_gas_used()
        print(input_str, r.output, expected_output, gas_post - gas_pre)
        assert r.is_success
        assert r.output == expected_output

def test_hex2(hex2_contract):
    for input_str, expected_output in HEX2_TESTCASES:
        with boa.env.anchor():
            r = boa.env.raw_call(to_address=hex2_contract, data=input_str.encode())
            assert r.is_success
            assert r.output == expected_output
