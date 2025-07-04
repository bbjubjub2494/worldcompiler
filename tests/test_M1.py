import boa

## FIXME duplicate of test_hex0.py, should be merged
HEX0_TESTCASES = [
    ("", b""),
    ("00", b"00"),
    ("10", b"10"),
    ("98", b"98"),
    (" AB", b"AB"),
    ("xAB", b"xAB"),
    ("ab # comment\n cd", b"abcd"),
    ("ABCD", b"ABCD"),
    ("AB CD EF # comment", b"ABCDEF"),
]

HEX2_TESTCASES = HEX0_TESTCASES + [
    (":label 00", b":label 00"),
    ("a :label b", b"a :label b"),
    ("cdef :something", b"cdef :something"),
    (":a ab +a", b"a ab +a"),
    ("ab :label +label", "ab :label +label"),
    ("ab +label :label", "ab +label :label"),
]

def test_M1(M1_contract):
    for input_str, expected_output in HEX2_TESTCASES:
        with boa.env.anchor():
            r = boa.env.raw_call(to_address=M1_contract, data=input_str.encode())
            assert r.is_success
            print(input_str, r.output, expected_output)
            assert r.output == expected_output
