import functools
import json
import pathlib
import subprocess

from solc_select import solc_select  # type: ignore


@functools.cache
def get_solc(solc_version):
    if not solc_select.install_artifacts([solc_version]):
        raise Exception(f"Failed to install solc version {solc_version}")
    return solc_select.artifact_path(solc_version)


def compile_sol(src, contract_name, solc_version="0.8.28", solc_opts=[]):
    try:
        src = pathlib.Path(src)
        # solc output uses relative paths if possible
        src = src.relative_to(src.cwd())
    except ValueError:
        pass
    solc = get_solc(solc_version)
    data = json.loads(
        subprocess.run(
            [solc, "--combined-json", "bin", "--input-file", src, *solc_opts],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
    )
    return bytes.fromhex(data["contracts"][f"{src}:{contract_name}"]["bin"])


def compile_yul(src, contract_name, solc_version="0.8.28"):
    solc = get_solc(solc_version)
    input_data = json.dumps({
        "language": "Yul",
        "sources": {
            str(src.name): {
                "content": src.read_text(encoding="utf-8"),
            },
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                    "abi",
                    "evm.bytecode.object",
                    ],
                },
            },
        },
    })
    data = json.loads(
        subprocess.run(
            [solc, "--standard-json"],
            check=True,
            input=input_data.encode("utf-8"),
            stdout=subprocess.PIPE,
        ).stdout
    )
    for err in data['errors']:
        print(err['formattedMessage'])
    return bytes.fromhex(data["contracts"][str(src.name)][contract_name]["evm"]["bytecode"]["object"])
