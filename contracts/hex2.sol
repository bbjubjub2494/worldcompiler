// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

struct ParserState {
    uint256 next_offset;
    uint256 tok; // first byte of token or EOF
    bytes32 label_hash;
}

uint256 constant TOK_EOF = 0x100;
uint8 constant TOK_hash = 35; // '#'
uint8 constant TOK_plus = 43; // '+'
uint8 constant TOK_colon = 58; // ':'
uint8 constant TOK_semicolon = 59; // ';'
uint8 constant TOK_underscore = 95; // '_'

uint8 constant TOK_0 = 48; // '0'
uint8 constant TOK_9 = 57; // '9'
uint8 constant TOK_A = 65; // 'A'
uint8 constant TOK_F = 70; // 'F'
uint8 constant TOK_Z = 90; // 'Z'
uint8 constant TOK_a = 97; // 'a'
uint8 constant TOK_f = 102; // 'f'
uint8 constant TOK_z = 122; // 'z'

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
        if (is_hexdigit(uint8(state.tok))) {
            // valid hex digit
            nibble_count++;
        } else if (state.tok == TOK_colon) {
            // no transient mapping in Solidity
            // convention: use the hash of the label as the slot
            // this contract has nothing else to store so no collision risk
            tstore(state.label_hash, nibble_count / 2);
        } else if (state.tok == TOK_plus) {
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
        uint8 c = uint8(state.tok);
        if (c >= TOK_0 && c <= TOK_9) {
            hold |= state.tok - TOK_0;
        } else if (c >= TOK_A && c <= TOK_F) {
            hold |= state.tok - TOK_A + 10;
        } else if (c >= TOK_a && c <= TOK_f) {
            hold |= state.tok - TOK_a + 10;
        } else if (state.tok == TOK_plus) {
            uint256 offset = tload(state.label_hash);
            output = bytes.concat(output, bytes1(uint8(offset)));
            continue;
        } else {
            continue;
        }
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

function next_token(ParserState memory state, bytes calldata input) pure {
    for (uint256 i = state.next_offset; i < input.length; i++) {
        uint8 c = uint8(input[i]);
        if (is_hexdigit(c)) {
            state.tok = c;
            state.next_offset = i + 1;
            return;
        } else if (c == TOK_semicolon || c == TOK_hash) {
            // comments: skip to end of line
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if (c == 13 || c == 10) {
                    // '\r' or '\n'
                    break;
                }
            }
        } else if (c == TOK_colon || c == TOK_plus) {
            // label or pointer
            state.tok = c;
            uint256 label_start = i + 1;
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if ((c < TOK_a || c > TOK_z) && c != TOK_underscore) {
                    break;
                }
            }
            state.label_hash = keccak256(input[label_start:i]);
            state.next_offset = i;
            return;
        }
    }
    state.tok = TOK_EOF;
}

function is_hexdigit(uint8 c) pure returns (bool) {
    return (c >= TOK_0 && c <= TOK_9) || (c >= TOK_A && c <= TOK_F) || (c >= TOK_a && c <= TOK_f);
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
