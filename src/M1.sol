// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

struct ParserState {
    uint256 next_offset;
    uint256 start_offset; // start of token content
    uint256 end_offset; // end of token content
    uint256 tok; // first byte of token or EOF
}

uint256 constant TOK_EOF = 0x100;
uint8 constant TOK_hash = 35; // '#'
uint8 constant TOK_semicolon = 59; // ';'
uint8 constant TOK_single_quote = 39; // '\''
uint8 constant TOK_double_quote = 34; // '"'
uint8 constant TOK_space = 32; // ' '
uint8 constant TOK_tab = 9; // '\t'
uint8 constant TOK_newline = 10; // '\n'
uint8 constant TOK_carriage_return = 13; // '\r'
uint8 constant TOK_plus = 43; // '+'
uint8 constant TOK_colon = 58; // ':'

uint8 constant TOK_0 = 48; // '0'
uint8 constant TOK_9 = 57; // '9'
uint8 constant TOK_A = 65; // 'A'
uint8 constant TOK_F = 70; // 'F'
uint8 constant TOK_Z = 90; // 'Z'
uint8 constant TOK_a = 97; // 'a'
uint8 constant TOK_f = 102; // 'f'
uint8 constant TOK_z = 122; // 'z'

contract M1 {
    bool private transient dirty;

    fallback(bytes calldata input) external returns (bytes memory output) {
        require(!dirty, "M1: dirty transient storage");
        dirty = true;
        return parse(input);
    }

    function parse(bytes calldata input) internal returns (bytes memory output) {
        ParserState memory state;
        bool first_output = true;
        
        for (next_token(state, input); state.tok != TOK_EOF; next_token(state, input)) {
            if (state.tok == TOK_single_quote) {
                // Handle single-quoted literal strings
                bytes memory literal = input[state.start_offset:state.end_offset];
                if (!first_output) {
                    output = bytes.concat(output, " ");
                }
                output = bytes.concat(output, literal);
                first_output = false;
            } else if (state.tok == TOK_double_quote) {
                // Handle double-quoted hex-encoded strings
                bytes memory hex_string = input[state.start_offset:state.end_offset];
                bytes memory encoded = hex_encode(hex_string);
                if (!first_output) {
                    output = bytes.concat(output, " ");
                }
                output = bytes.concat(output, encoded);
                first_output = false;
            } else if (is_define_token(state, input)) {
                // Handle DEFINE statements
                handle_define(state, input);
            } else if (is_atom_start(uint8(state.tok))) {
                // Handle atoms (including special atoms and defined names)
                bytes memory atom = input[state.start_offset:state.end_offset];
                bytes memory resolved = resolve_atom(atom);
                if (!first_output) {
                    output = bytes.concat(output, " ");
                }
                output = bytes.concat(output, resolved);
                first_output = false;
            }
        }
        
        return output;
    }

    function next_token(ParserState memory state, bytes calldata input) internal pure {
        // Skip whitespace
	for (uint256 i = state.next_offset; i < input.length; i++) {
		uint8 c = uint8(input[i]);
        if (c == TOK_hash || c == TOK_semicolon) {
            // comments: skip to end of line
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if (c == 13 || c == 10) {
                    // '\r' or '\n'
                    break;
                }
            }
        } else if (c == TOK_single_quote || c == TOK_double_quote) {
            state.tok = c;
            state.start_offset = i + 1;
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if (c == state.tok) {
                    break;
                }
            }
	    state.end_offset = i;
	    state.next_offset = i + 1;
	    return;
        } else if (is_atom_start(c)) {
            state.tok = c;
            state.start_offset = i;
            for (i++; i < input.length; i++) {
                c = uint8(input[i]);
                if (is_whitespace(c)) {
                    break;
                }
	    }
		state.end_offset = i;
	    	state.next_offset = i;
		return;
            }
	    // ignore other characters
	}
	state.tok = TOK_EOF;
    }

    function is_define_token(ParserState memory state, bytes calldata input) internal pure returns (bool) {
        uint256 start = state.start_offset;
        uint256 end = state.end_offset;
        
        if (start + 6 != end) {
	    return false; // Not enough characters for "DEFINE"
	}
        
        return bytes6(input[start:end]) == bytes6("DEFINE");
    }

    function handle_define(ParserState memory state, bytes calldata input) internal {
        next_token(state, input);
        bytes memory name = input[state.start_offset:state.end_offset];
        bytes32 name_hash = keccak256(name);
        
        next_token(state, input);
        bytes memory value =  input[state.start_offset:state.end_offset];
        
        tstore(name_hash, bytes32(value));
    }

    function resolve_atom(bytes memory atom) internal view returns (bytes memory) {
        bytes32 atom_hash = keccak256(atom);
        bytes32 value = tload(atom_hash);

	if (value == bytes32(0)) {
	    // not defined
	    return atom;
	}
        
        // Convert back to bytes
        bytes memory result = new bytes(32);
        assembly {
            mstore(add(result, 0x20), value)
        }
        
        // Find actual length by looking for null terminator
        uint256 actual_length = 0;
        for (uint256 i = 0; i < 32; i++) {
            if (result[i] == 0) break;
            actual_length++;
        }
        
        // Resize to actual length
        assembly {
            mstore(result, actual_length)
        }
        
        return result;
    }

    function hex_encode(bytes memory input) internal pure returns (bytes memory) {
        bytes memory result = new bytes(input.length * 2);
        bytes memory alphabet = "0123456789abcdef";
        
        for (uint256 i = 0; i < input.length; i++) {
            result[i * 2] = alphabet[uint8(input[i]) >> 4];
            result[i * 2 + 1] = alphabet[uint8(input[i]) & 0x0f];
        }
        
        return result;
    }

    function is_whitespace(uint8 c) internal pure returns (bool) {
        return c == TOK_space || c == TOK_tab || c == TOK_newline || c == TOK_carriage_return;
    }

    function is_atom_start(uint8 c) internal pure returns (bool) {
        return is_alphanumeric(c) || is_special_char(c);
    }

    function is_atom_char(uint8 c) internal pure returns (bool) {
        return is_alphanumeric(c) || is_special_char(c);
    }

    function is_alphanumeric(uint8 c) internal pure returns (bool) {
        return (c >= TOK_0 && c <= TOK_9) || 
               (c >= TOK_A && c <= TOK_Z) || 
               (c >= TOK_a && c <= TOK_z);
    }

    function is_special_char(uint8 c) internal pure returns (bool) {
        return c == TOK_plus || c == TOK_colon;
    }

    function tstore(bytes32 key, bytes32 value) internal {
        assembly {
            tstore(key, value)
        }
    }

    function tload(bytes32 key) internal view returns (bytes32 value) {
        assembly {
            value := tload(key)
        }
    }
}
