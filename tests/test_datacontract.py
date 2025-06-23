import boa

def test_simple(datacontract_initcode_prefix):
    data = b"test"
    bytecode = datacontract_initcode_prefix + data
    addr, _ = boa.env.deploy_code(bytecode=bytecode)
    assert boa.env.get_code(addr) == data

def test_erc7955(erc7955_factory, datacontract_initcode_prefix):
    data = b"test"
    bytecode = datacontract_initcode_prefix + data
    addr = erc7955_factory.deploy(bytecode)
    assert boa.env.get_code(addr) == data
