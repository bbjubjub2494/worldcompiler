import importlib.resources, subprocess

from ethbootstrap_languages import Hex2Parser

files = importlib.resources.files(__package__)

def compile_M1(src):
    with importlib.resources.as_file(files/ "evm_defs.M1") as defs:
        r = subprocess.run(
            ["M1", "-f", defs, "-f", "/dev/stdin"],
            input=src.read_bytes(),
            stdout=subprocess.PIPE,
            check=True,
        )
    return r.stdout

def compile_hex2(src):
    if not isinstance(src, bytes):
        src = src.read_bytes()
    return Hex2Parser.parse(src)

hex0_bytecode = compile_hex2(compile_M1(files / "hex0.M1"))
trivial_initcode_prefix = compile_hex2(files / "trivial_initcode_prefix.hex2")

__all__ = [ "hex0_bytecode" ]
