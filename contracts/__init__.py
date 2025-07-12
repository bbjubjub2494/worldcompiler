import subprocess
from pathlib import Path

from ethbootstrap_languages import Hex2Parser

def load_datacontract_initcode_prefix():
    # FIXME: hardcoded path
    f = compile_hex2("contracts/datacontract_initcode_prefix.hex2")
    return f.read_bytes()

def load_inputaddressed_initcode_template():
    f = compile_M1("contracts/inputaddressed_initcode_template.M1")
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
    dst.write_bytes(Hex2Parser.parse(src.read_bytes()))
    return dst
