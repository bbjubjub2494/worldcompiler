import boa
from boa.util.abi import abi_encode
from vyper.utils import keccak256


def test_registry(registry_contract, fibonacci_contract):
    input_data = fibonacci_contract.fib.prepare_calldata(4)
    expected_output = abi_encode("uint256", 5)

    r = registry_contract.get(
        keccak256(fibonacci_contract.bytecode), keccak256(input_data)
    )
    assert r == bytes(32)

    r = registry_contract.register(fibonacci_contract.address, input_data)
    assert r is True

    r = registry_contract.get(
        keccak256(fibonacci_contract.bytecode), keccak256(input_data)
    )
    assert r == keccak256(expected_output)

    r = registry_contract.register(fibonacci_contract.address, input_data)
    assert r is False


def test_bad_functions(registry_contract):
    identity_precompile = "4".rjust(40, "0")

    with boa.reverts("empty function"):
        registry_contract.register(identity_precompile, b"test")

    # Make account empty (codehash=keccak256("")) instead of nonexistent (codehash=0)
    boa.env.raw_call(to_address=identity_precompile, value=1)

    with boa.reverts("empty function"):
        registry_contract.register(identity_precompile, b"test")
