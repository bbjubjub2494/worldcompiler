import boa
from boa.util.abi import Address

import functools, importlib.resources

from util import compile_sol

# per ERC-7744
solc_version = "0.8.28"
solc_opts = [
    "--optimize",
    "--optimize-runs", "2000",
    "--metadata-hash", "none",
    "--via-ir",
    "--optimize-yul",
]
deployment_salt = bytes.fromhex("9425035d50edcd7504fe5eeb5df841cc74fe6cccd82dca6ee75bcdf774bd88d9")
arachnid_deployer_address = "0x4e59b44847b379578588920ca78fbf26c0b4956c"
arachnid_deployer_bytecode = bytes.fromhex("7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe03601600081602082378035828234f58015156039578182fd5b8082525050506014600cf3")

@functools.cache
def get_bytecode():
    with importlib.resources.as_file(importlib.resources.files(__package__) / "ERC7744.sol") as src:
        return compile_sol(src, "ERC7744", solc_version, solc_opts)

def deploy():
    boa.env.set_code(arachnid_deployer_address, arachnid_deployer_bytecode)
    r = boa.env.raw_call(to_address=arachnid_deployer_address, data=deployment_salt+get_bytecode())
    return Address(r.output)
