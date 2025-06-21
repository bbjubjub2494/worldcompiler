import boa

def test_empty(datacontract_initcode_prefix):
    data = b"test"
    bytecode = datacontract_initcode_prefix + data
    addr, _ = boa.env.deploy_code(bytecode=bytecode)
    print(data, boa.env.get_code(addr))
    assert boa.env.get_code(addr) == data
