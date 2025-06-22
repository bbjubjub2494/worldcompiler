import subprocess
from pathlib import Path
import tempfile

def load_datacontract_initcode_prefix():
    # FIXME: hardcoded path
    r = subprocess.run(
        ("hex2", "-f", "src/datacontract_initcode_prefix.hex2"),
        check=True,
        stdout=subprocess.PIPE,
    )
    return r.stdout

def load_inputaddressed_initcode_template():
    return compile_M2("src/inputaddressed_initcode_template.M1")

def compile_M2(src):
    src = Path(src)
    with tempfile.NamedTemporaryFile(
        prefix=f".{src.stem}", suffix='.hex2', dir=src.parent
    ) as tmp_hex2:
        subprocess.run(
            ("M1", "-f", "src/evm_defs.M1", "-f", src, "-o", tmp_hex2.name),
            check=True,
        )
        return subprocess.run(
            ("hex2", "-f", tmp_hex2.name),
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
