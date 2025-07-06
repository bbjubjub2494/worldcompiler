#pragma version 0.4.3

output_hash: HashMap[bytes32, HashMap[bytes32, bytes32]]

error NotFound()

@external
def register(
    function: address,
    input: Bytes[1_000_000],
):
    function_codehash: bytes32 = function.codehash
    input_hash: bytes32 = keccak256(input)

    output: Bytes[1_000_000] = raw_call(function, input, max_outsize=1_000_000)

    self.output[function_codehash][input_hash] = keccak256(output)

@external
def get(
    function_codehash: bytes32,
    input_hash: bytes32,
) -> bytes32:
    output_hash: bytes32 = self.result_hash[function_codehash][input_hash]
    if output_hash == empty(bytes32):
        raise NotFound()
    return output_hash
