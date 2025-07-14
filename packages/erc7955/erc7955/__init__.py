import boa  # type: ignore

from boa.util.abi import Address, abi_decode  # type: ignore

from ethbootstrap_util import create2_address_of

__all__ = [
    "factory_deploy",
    "factory_address",
    "factory_bytecode",
    "factory_predict_address",
]

factory_address: Address = Address("0xC0DE945918F144DcdF063469823a4C51152Df05D")
factory_bytecode: bytes = bytes.fromhex(
    "60203d3d3582360380843d373d34f580601457fd5b3d52f3"
)


def factory_deploy(initcode: bytes, deployment_salt: bytes = bytes(32)) -> Address:
    if len(deployment_salt) != 32:
        raise ValueError("Deployment salt must be exactly 32 bytes long")
    boa.env.set_code(factory_address, factory_bytecode)

    data = deployment_salt + initcode
    r = boa.env.raw_call(to_address=factory_address, data=data)

    return abi_decode("address", r.output)


def factory_predict_address(
    initcode: bytes, deployment_salt: bytes = bytes(32)
) -> Address:
    if len(deployment_salt) != 32:
        raise ValueError("Deployment salt must be exactly 32 bytes long")
    return create2_address_of(factory_address, deployment_salt, initcode)
