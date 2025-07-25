#pragma version 0.4.3

output_hash: HashMap[bytes32, HashMap[bytes32, bytes32]]

@external
def register(
    function: address,
    input: Bytes[1_000_000],
) -> bool:
    function_codehash: bytes32 = function.codehash
    input_hash: bytes32 = keccak256(input)

    if function_codehash in [keccak256(""), empty(bytes32)]:
        raise "empty function"

    if self.output_hash[function_codehash][input_hash] != empty(bytes32):
        return False  # Already registered

    output: Bytes[1_000_000] = raw_call(function, input, max_outsize=1_000_000)

    self.output_hash[function_codehash][input_hash] = keccak256(output)
    return True

@external
def get(
    function_codehash: bytes32,
    input_hash: bytes32,
) -> bytes32:
    output_hash: bytes32 = self.output_hash[function_codehash][input_hash]
    return output_hash
