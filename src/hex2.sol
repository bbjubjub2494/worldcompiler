// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

struct ParserState {
    uint256 next_offset;
    uint8 tok; // current token: 0-15 for hex digits, TOK_* values otherwise
    bytes32 label_hash;
}

uint8 constant TOK_LABEL = 0x10; // arbitrary string label
uint8 constant TOK_POINTER1 = 0x11; // 1-byte, absolute pointer to label
uint8 constant TOK_EOF = 0xff;

contract hex2 {
    bool private transient dirty;

    fallback(bytes calldata input) external returns (bytes memory output) {
        require(!dirty, "hex2: dirty transient storage");
        dirty = true;
        first_pass(input);
        return second_pass(input);
    }
}

function first_pass(bytes calldata input) {
    uint256 nibble_count = 0;
    ParserState memory state;

    for (next_token(state, input); state.tok != TOK_EOF; next_token(state, input)) {
        if (state.tok < 16) {
            // valid hex digit
            nibble_count++;
        } else if (state.tok == TOK_LABEL) {
            // no transient mapping in Solidity
            // convention: use the hash of the label as the slot
            // this contract has nothing else to store so no collision risk
            tstore(state.label_hash, nibble_count / 2);
        } else if (state.tok == TOK_POINTER1) {
            // 1 byte = 2 nibbles
            nibble_count += 2;
        }
    }
}

function second_pass(bytes calldata input) view returns (bytes memory output) {
    bool toggle = false;
    uint256 hold = 0;

    ParserState memory state;
    for (next_token(state, input); state.tok != TOK_EOF; next_token(state, input)) {
        if (state.tok < 16) {
            // valid hex digit
            hold |= state.tok;
            if (toggle) {
                output = bytes.concat(output, bytes1(uint8(hold)));
                hold = 0;
                toggle = false;
            } else {
                hold <<= 4;
                toggle = true;
            }
        } else if (state.tok == TOK_POINTER1) {
            uint256 offset = tload(state.label_hash);
            output = bytes.concat(output, bytes1(uint8(offset)));
        }
    }
}

function next_token(ParserState memory state, bytes calldata input) pure {
    for (uint256 i = state.next_offset; i < input.length; i++) {
        uint8 c = uint8(input[i]);
        if (c >= 97 && c <= 102) {
            // 'a' to 'f'
            state.tok = c - 87;
            state.next_offset = i + 1;
            return;
        } else if (c >= 48 && c <= 57) {
            // '0' to '9'
            state.tok = c - 48;
            state.next_offset = i + 1;
            return;
        } else if (c >= 65 && c <= 70) {
            // 'A' to 'F'
            state.tok = c - 55;
            state.next_offset = i + 1;
            return;
        } else if (c == 59 || c == 35) {
            // ';' or '#' - comment handling
            // Skip to end of line
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if (c == 13 || c == 10) {
                    // '\r' or '\n'
                    break;
                }
            }
        } else if (c == 58) {
            // ':' - label
            uint256 label_start = i + 1;
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if ((c < 97 || c > 122) && c != 95) {
                    // not 'a' to 'z'
                    break;
                }
            }
            state.tok = TOK_LABEL;
            state.label_hash = keccak256(input[label_start:i]);
            state.next_offset = i;
            return;
        } else if (c == 43) {
            // '+' - 1-byte pointer (not in normal hex2, custom EVM extension)
            // FIXME duplication
            uint256 label_start = i + 1;
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if ((c < 97 || c > 122) && c != 95) {
                    // not 'a' to 'z'
                    break;
                }
            }
            state.tok = TOK_POINTER1;
            state.label_hash = keccak256(input[label_start:i]);
            state.next_offset = i;
            return;
        }
    }
    state.tok = TOK_EOF;
}

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
