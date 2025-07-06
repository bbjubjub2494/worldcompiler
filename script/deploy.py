from contracts import load_datacontract_initcode_prefix, load_hex0, InputAddressedRegistry

import boa

import json
import subprocess

def deploy_hex0_ref():
    initcode = compile_sol("contracts/hex0.sol", "hex0")
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def deploy_hex0():
    code = load_hex0()
    datacontract_initcode_prefix = load_datacontract_initcode_prefix()
    initcode = datacontract_initcode_prefix + code
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def deploy_hex2():
    initcode = compile_sol("contracts/hex2.sol", "hex2")
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def deploy_M1():
    initcode = compile_sol("contracts/M1.sol", "M1")
    address, _ = boa.env.deploy_code(bytecode=initcode)
    return address

def deploy_InputAddressedRegistry():
    return InputAddressedRegistry.deploy()

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
    deploy_M1()
    deploy_InputAddressedRegistry()
