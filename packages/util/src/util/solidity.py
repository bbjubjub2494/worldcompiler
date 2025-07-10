import functools, json, pathlib, subprocess

from solc_select import solc_select

@functools.cache
def get_solc(solc_version):
    if not solc_select.install_artifacts([solc_version]):
        raise Error(f"Failed to install solc version {solc_version}")
    return solc_select.artifact_path(solc_version)

def compile_sol(src, contract_name, solc_version="0.8.28", solc_opts=[]):
    try:
        src = pathlib.Path(src)
        # solc output uses relative paths if possible
        src = src.relative_to(src.cwd())
    except ValueError:
        pass
    solc = get_solc(solc_version)
    data = json.loads(subprocess.run([
            solc,
            "--combined-json", "bin",
            "--input-file", src,
            *solc_opts],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout)
    return bytes.fromhex(data["contracts"][f"{src}:{contract_name}"]["bin"])
