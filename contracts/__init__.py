import subprocess
from pathlib import Path

def load_datacontract_initcode_prefix():
    # FIXME: hardcoded path
    f = compile_hex2("contracts/datacontract_initcode_prefix.hex2")
    return f.read_bytes()

def load_inputaddressed_initcode_template():
    f = compile_M1("contracts/inputaddressed_initcode_template.M1")
    f = compile_hex2(f)
    return f.read_bytes()

def load_hex0():
    f = compile_M1("contracts/hex0.M1")
    f = compile_hex2(f)
    return f.read_bytes()

def compile_M1(src):
    src = Path(src)
    dst = Path(f"build/{src.stem}.hex2")
    subprocess.run(
        ("M1", "-f", "contracts/evm_defs.M1", "-f", src, "-o", dst),
        check=True,
    )
    return dst

def compile_hex2(src):
    src = Path(src)
    dst = Path(f"build/{src.stem}.bin")
    subprocess.run(
        ("hex2", "-f", src, "-o", dst),
        check=True,
    )
    return dst
