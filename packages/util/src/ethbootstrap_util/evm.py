from boa.util.abi import Address  # type: ignore
from vyper.utils import keccak256  # type: ignore


def create2_address_of(factory: Address, salt: bytes, initcode: bytes) -> Address:
    if len(salt) != 32:
        raise ValueError("Salt must be exactly 32 bytes long")

    initcode_hash = keccak256(initcode)
    return Address(
        keccak256(b"\xff" + bytes.fromhex(factory[2:]) + salt + initcode_hash)[12:]
    )
