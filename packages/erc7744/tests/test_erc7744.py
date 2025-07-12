import boa

import erc7744


def test_get_bytecode():
    bytecode = erc7744.get_bytecode()
    assert isinstance(bytecode, bytes)
    assert len(bytecode) > 0


def test_deploy():
    expected_deployment_address = "0xC0De1D1126b6D698a0073A4e66520111cEe22F62"
    address = erc7744.deploy()
    assert address == expected_deployment_address
    assert erc7744.get_bytecode().endswith(boa.env.get_code(address))
