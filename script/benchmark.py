import boa

from script.deploy import deploy_hex0, deploy_hex2, deploy_M1

from pathlib import Path

def moccasin_main():
    hex0 = deploy_hex0()
    hex2 = deploy_hex2()
    M1 = deploy_M1()

    build = Path("build")
    contracts = Path("contracts")

    input_bytes = (contracts/"evm_defs.M1").read_bytes() + (contracts/"hex0.M1").read_bytes()
    r = boa.env.raw_call(to_address=M1, data=input_bytes)
    assert r.is_success
    print(f"M1:\t{r.get_gas_used()}")

    input_bytes = (build/"hex0.hex2").read_bytes()
    r = boa.env.raw_call(to_address=hex2, data=input_bytes)
    assert r.is_success
    print(f"hex2:\t{r.get_gas_used()}")
