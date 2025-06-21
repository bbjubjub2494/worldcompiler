import subprocess

def load_datacontract_initcode_prefix():
    # FIXME: hardcoded path
    r = subprocess.run(
        ("hex2", "-f", "src/datacontract_initcode_prefix.hex2"),
        check=True,
        stdout=subprocess.PIPE,
    )
    return r.stdout
