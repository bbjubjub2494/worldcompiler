from src import load_datacontract_initcode_prefix

import boa

import json
import subprocess

def deploy_hex0():
    initcode = compile_sol("src/hex0.sol", "hex0")
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def deploy_hex2():
    initcode = compile_sol("src/hex2.sol", "hex2")
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def compile_sol(src, contract_name):
    datacontract_initcode_prefix = load_datacontract_initcode_prefix()
    data = json.loads(subprocess.run(
        ("solc", "--combined-json=bin", src),
        check=True,
        stdout=subprocess.PIPE,
    ).stdout)
    return bytes.fromhex(data["contracts"][f"{src}:{contract_name}"]["bin"])

def moccasin_main():
    deploy_hex0()
    deploy_hex2()
