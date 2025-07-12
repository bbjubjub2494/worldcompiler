import boa

from boa.util.abi import Address

factory_address = "0xC0DE207acb0888c5409E51F27390Dad75e4ECbe7"
factory_bytecode = bytes.fromhex("60203d3d3582360380843d373d34f580601457fd5b3d52f3")


def factory_deploy(initcode: bytes, deployment_salt: bytes = bytes(32)) -> Address:
    boa.env.set_code(factory_address, factory_bytecode)

    data = deployment_salt + initcode
    r = boa.env.raw_call(to_address=factory_address, data=data)

    return abi_decode("address", r.output)
