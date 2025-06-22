import subprocess

def load_datacontract_initcode_prefix():
    # FIXME: hardcoded path
    r = subprocess.run(
        ("hex2", "-f", "src/datacontract_initcode_prefix.hex2"),
        check=True,
        stdout=subprocess.PIPE,
    )
    return r.stdout

def load_inputaddressed_initcode_template():
    r = subprocess.run(
        ("M1", "-f", "src/evm_defs.M1", "-f", "src/inputaddressed_initcode_template.M1"),
        check=True,
        stdout=subprocess.PIPE,
    )
    r = subprocess.run(
        ("hex2"),
        check=True,
        stdin=r.stdout,
        stdout=subprocess.PIPE,
    )
    return r.stdout

print(load_inputaddressed_initcode_template())
