from src import load_datacontract_initcode_prefix

import boa

import json
import subprocess

def deploy_hex0():
    datacontract_initcode_prefix = load_datacontract_initcode_prefix()
    data = json.loads(subprocess.run(
        ("solc", "--combined-json=bin", "src/hex0.sol"),
        check=True,
        stdout=subprocess.PIPE,
    ).stdout)
    initcode = bytes.fromhex(data["contracts"]["src/hex0.sol:hex0"]["bin"])
    initcode += datacontract_initcode_prefix.ljust(32, b'\0')
    print(initcode)
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def moccasin_main():
    return deploy()
