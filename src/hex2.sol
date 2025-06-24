// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

uint8 constant LABEL = 0x10;
uint8 constant EOF = 0xff;

struct ParserState {
    uint256 next_offset;
    uint8 tok; // current token: 0-15 for hex digits, LABEL for labels
    bytes32 label_hash;
}


// no transient mapping in Solidity, so we just roll it
// convention: use the hash of the label as the slot
// this contract has nothing else to store so no collision risk
function tstore(bytes32 key, uint256 value) {
	assembly {
	tstore(key, value)
    }
}

function tload(bytes32 key) view returns (uint256 value) {
	assembly {
	value := tload(key)
    }
}

contract hex2 {
    bool private transient dirty;

    fallback(bytes calldata input) external returns (bytes memory output) {
	require(!dirty, "hex2: dirty transient storage");
        dirty = true;
	first_pass(input);
	return second_pass(input);
    }

    function next_token(ParserState memory state, bytes calldata input) internal pure {
	for (uint i = state.next_offset; i < input.length; i++) {
            uint8 c = uint8(input[i]);
            if (c >= 97 && c <= 102) { // 'a' to 'f'
		    state.tok = c - 87;
		    state.next_offset = i+1;
		    return;
	    } else if (c >= 48 && c <= 57) { // '0' to '9'
		    state.tok = c - 48;
		    state.next_offset = i+1;
		    return;
	    } else if (c >= 65 && c <= 70) { // 'A' to 'F'
		    state.tok = c - 55;
		    state.next_offset = i+1;
		    return;
	    } else if (c == 59 || c == 35) { // ';' or '#' - comment handling
                // Skip to end of line
                for (i++; i < input.length; i++) {
                    c = uint8(input[i]);
                    if (c == 13 || c == 10) { // '\r' or '\n'
                        break;
                    }
                }
            } else if (c == 58) { // ':' - jump label
		uint label_start = i + 1;
                for (i++; i < input.length; i++) {
                    c = uint8(input[i]);
                    if (c < 97 || c > 122) { // not 'a' to 'z'
                        break;
                    }
                }
		state.tok = LABEL;
		state.label_hash = keccak256(input[label_start:i]);
		state.next_offset = i;
		return;
            }
	}
	state.tok = EOF;
    }

    function first_pass(bytes calldata input) internal {
        uint256 nibble_count = 0;
	ParserState memory state;
        
	for (next_token(state, input); state.tok != EOF; next_token(state, input)) {
            if (state.tok < 16) { // valid hex digit
		nibble_count++;
	    } else if (state.tok == LABEL) {
		tstore(state.label_hash, nibble_count / 2);
	    } else if (state.tok < 16) {
		    nibble_count++;
            }
	}
    }

    function second_pass(bytes calldata input) internal view returns (bytes memory output) {
	    bool toggle = false;
	    uint256 hold = 0;

	ParserState memory state;
	for (next_token(state, input); state.tok != EOF; next_token(state, input)) {
            if (state.tok < 16) { // valid hex digit
		    hold |= state.tok;
            if (toggle) {
                output = bytes.concat(output, bytes1(uint8(hold)));
                hold = 0;
                toggle = false;
            } else {
                hold <<= 4;
                toggle = true;
            }
	    }
        }
    }
}
