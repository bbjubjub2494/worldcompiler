import boa  # type: ignore

from boa.util.abi import Address  # type: ignore

proxy_address = "0x4e59b44847b379578588920ca78fbf26c0b4956c"
proxy_bytecode = bytes.fromhex(
    "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0"
    "3601600081602082378035828234f58015156039578182fd5b8082525050506014"
    "600cf3"
)


def proxy_deploy(initcode: bytes, deployment_salt: bytes = bytes(32)) -> Address:
    boa.env.set_code(proxy_address, proxy_bytecode)

    data = deployment_salt + initcode
    r = boa.env.raw_call(to_address=proxy_address, data=data)

    # note: this works because the proxy does not left-pad its output.
    # if it did, we would need to use `abi.decode`.
    return Address(r.output)
