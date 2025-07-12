import boa
from boa.util.abi import Address

import functools, importlib.resources

from util import compile_sol
from deterministic_deployment_proxy import proxy_deploy

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

@functools.cache
def get_bytecode():
    with importlib.resources.as_file(importlib.resources.files(__package__) / "ERC7744.sol") as src:
        return compile_sol(src, "ERC7744", solc_version, solc_opts)

def deploy():
    return proxy_deploy(get_bytecode(), deployment_salt=deployment_salt)
