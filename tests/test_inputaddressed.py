import boa

PUSH20 = 0x73
IDENTITY_ADDRESS = b"\0"*19 + b"\4"

def test_program_offset(inputaddressed_initcode_template):
    '''
    The program starts with a push of the address of the function,
    represented by the identity precompile address.
    This test checks that this wasn't accidentally changed.
    '''
    assert inputaddressed_initcode_template.startswith(bytes([PUSH20, *IDENTITY_ADDRESS]))

def test_inputaddressed_identity(inputaddressed_initcode_template):
    identity = bytes.fromhex("365f5f37365ff3")  # identity contract per EIP-7666
    boa.env.set_code(IDENTITY_ADDRESS, identity)
    #TODO boa.deregister_precompile(IDENTITY_ADDRESS)

    data = b"test"
    bytecode = bytearray(inputaddressed_initcode_template)
    bytecode[1:21] = IDENTITY_ADDRESS
    addr, _ = boa.env.deploy_code(bytecode=bytes(bytecode+data))
    assert boa.env.get_code(addr) == data
