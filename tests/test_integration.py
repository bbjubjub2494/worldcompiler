from pathlib import Path

import boa

from collections import namedtuple

from vyper.utils import keccak256

def test_M1_compile_hex0(hex2_contract, M1_contract):
    build = Path("build")
    contracts = Path("contracts")

    input_bytes = (contracts/"evm_defs.M1").read_bytes() + (contracts/"hex0.M1").read_bytes()
    r = boa.env.raw_call(to_address=M1_contract, data=input_bytes)
    assert r.is_success

    input_bytes = r.output
    expected_output = (build/"hex0.bin").read_bytes()
    r = boa.env.raw_call(to_address=hex2_contract, data=input_bytes)
    assert r.is_success
    assert r.output == expected_output

def test_hex2_compile_hex0(hex2_contract, M1_contract):
    build = Path("build")

    input_bytes = (build/"hex0.hex2").read_bytes()
    expected_output = (build/"hex0.bin").read_bytes()
    r = boa.env.raw_call(to_address=hex2_contract, data=input_bytes)
    assert r.is_success
    assert r.output == expected_output

Node = namedtuple("Node", ["function", "input"])
Blob = namedtuple("Blob", ["content_hash"])

def get_output_hash(registry, el):
    if isinstance(el, Node):
        return registry.get(get_output_hash(registry, el.function), get_output_hash(registry, el.input))
    else:
        return el.content_hash

def test_verifier(hex2_contract, M1_contract, inputaddressed_registry):
    contracts = Path("contracts")
    build = Path("build")

    input_bytes = (contracts/"evm_defs.M1").read_bytes() + (contracts/"hex0.M1").read_bytes()
    expected_output_hash = keccak256((build/"hex0.bin").read_bytes())

    with boa.env.anchor():
        r = boa.env.raw_call(to_address=M1_contract, data=input_bytes)
        assert r.is_success
        hex2_bytes = r.output

    def code_hash(address):
        return keccak256(boa.env.get_code(address))
    graph = Node(Blob(code_hash(hex2_contract)),
    Node(Blob(code_hash(M1_contract)), Blob(keccak256(input_bytes))))

    inputaddressed_registry.register(M1_contract, input_bytes)
    inputaddressed_registry.register(hex2_contract, hex2_bytes)

    output_hash = get_output_hash(inputaddressed_registry, graph)
    assert output_hash == expected_output_hash
