struct ParserState {
    uint256 next_offset;
    uint256 tok; // first byte of token or EOF
    bytes32 token_hash;
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
        
        for (next_token(state, input); state.tok != TOK_EOF; next_token(state, input)) {
            if (state.tok == TOK_single_quote) {
                // Handle single-quoted literal strings
                bytes memory literal = read_single_quoted_string(state, input);
                output = bytes.concat(output, literal);
            } else if (state.tok == TOK_double_quote) {
                // Handle double-quoted hex-encoded strings
                bytes memory hex_string = read_double_quoted_string(state, input);
                bytes memory encoded = hex_encode(hex_string);
                output = bytes.concat(output, encoded);
            } else if (is_define_token(state, input)) {
                // Handle DEFINE statements
                handle_define(state, input);
            } else if (is_atom_start(uint8(state.tok))) {
                // Handle atoms (including special atoms and defined names)
                bytes memory atom = read_atom(state, input);
                bytes memory resolved = resolve_atom(atom);
                output = bytes.concat(output, resolved);
            }
        }
        
        return output;
    }

    function next_token(ParserState memory state, bytes calldata input) internal pure {
        // Skip whitespace
        while (state.next_offset < input.length && is_whitespace(uint8(input[state.next_offset]))) {
            state.next_offset++;
        }
        
        if (state.next_offset >= input.length) {
            state.tok = TOK_EOF;
            return;
        }
        
        uint8 c = uint8(input[state.next_offset]);
        
        // Handle comments
        if (c == TOK_hash || c == TOK_semicolon) {
            skip_comment(state, input);
            next_token(state, input); // Recursively get next token after comment
            return;
        }
        
        // Handle strings
        if (c == TOK_single_quote || c == TOK_double_quote) {
            state.tok = c;
            state.next_offset++;
            return;
        }
        
        // Handle atoms (including special atoms starting with special characters)
        if (is_atom_start(c)) {
            state.tok = c;
            return;
        }
        
        // Skip unknown characters
        state.next_offset++;
        next_token(state, input);
    }

    function skip_comment(ParserState memory state, bytes calldata input) internal pure {
        // Skip until end of line
        for (uint256 i = state.next_offset + 1; i < input.length; i++) {
            uint8 c = uint8(input[i]);
            if (c == TOK_newline || c == TOK_carriage_return) {
                state.next_offset = i + 1;
                return;
            }
        }
        state.next_offset = input.length;
    }

    function read_single_quoted_string(ParserState memory state, bytes calldata input) internal pure returns (bytes memory) {
        uint256 start = state.next_offset;
        uint256 i = start;
        
        // Find closing quote
        while (i < input.length && uint8(input[i]) != TOK_single_quote) {
            i++;
        }
        
        if (i < input.length) {
            i++; // Skip closing quote
        }
        
        bytes memory result = bytes.concat("'", input[start:i-1], "'");
        state.next_offset = i;
        return result;
    }

    function read_double_quoted_string(ParserState memory state, bytes calldata input) internal pure returns (bytes memory) {
        uint256 start = state.next_offset;
        uint256 i = start;
        
        // Find closing quote
        while (i < input.length && uint8(input[i]) != TOK_double_quote) {
            i++;
        }
        
        if (i < input.length) {
            i++; // Skip closing quote
        }
        
        bytes memory content = input[start:i-1];
        state.next_offset = i;
        return content;
    }

    function read_atom(ParserState memory state, bytes calldata input) internal pure returns (bytes memory) {
        uint256 start = state.next_offset;
        uint256 i = start;
        
        // Read atom characters
        while (i < input.length && is_atom_char(uint8(input[i]))) {
            i++;
        }
        
        bytes memory atom = input[start:i];
        state.next_offset = i;
        return atom;
    }

    function is_define_token(ParserState memory state, bytes calldata input) internal pure returns (bool) {
        uint256 start = state.next_offset;
        
        // Check if we have "DEFINE"
        if (start + 6 > input.length) return false;
        
        return (uint8(input[start]) == 68 && // 'D'
                uint8(input[start + 1]) == 69 && // 'E'
                uint8(input[start + 2]) == 70 && // 'F'
                uint8(input[start + 3]) == 73 && // 'I'
                uint8(input[start + 4]) == 78 && // 'N'
                uint8(input[start + 5]) == 69 && // 'E'
                (start + 6 >= input.length || is_whitespace(uint8(input[start + 6]))));
    }

    function handle_define(ParserState memory state, bytes calldata input) internal {
        // Skip "DEFINE"
        state.next_offset += 6;
        
        // Get name
        next_token(state, input);
        bytes memory name = read_atom(state, input);
        
        // Get value
        next_token(state, input);
        bytes memory value;
        
        if (state.tok == TOK_single_quote) {
            value = read_single_quoted_string(state, input);
        } else if (state.tok == TOK_double_quote) {
            bytes memory content = read_double_quoted_string(state, input);
            value = hex_encode(content);
        } else {
            value = read_atom(state, input);
        }
        
        // Store in transient storage
        bytes32 name_hash = keccak256(name);
        bytes32 value_hash = keccak256(value);
        tstore(name_hash, value_hash);
        tstore(value_hash, bytes32(value));
    }

    function resolve_atom(bytes memory atom) internal view returns (bytes memory) {
        bytes32 atom_hash = keccak256(atom);
        bytes32 value_hash = tload(atom_hash);
        
        if (value_hash == bytes32(0)) {
            // Not defined, return as-is
            return atom;
        }
        
        bytes32 stored_value = tload(value_hash);
        
        // Convert back to bytes
        bytes memory result = new bytes(32);
        assembly {
            mstore(add(result, 0x20), stored_value)
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
        return c == 43 || c == 58 || c == 45 || c == 95; // '+', ':', '-', '_'
    }

    function tstore(bytes32 key, uint256 value) internal {
        assembly {
            tstore(key, value)
        }
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
