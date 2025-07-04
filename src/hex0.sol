// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract hex0 {
    fallback(bytes calldata) external returns (bytes memory) {
        assembly {
            // Main entry point

            // Reserve memory for output (worst case: input_size / 2)
            let output_ptr := 0x80 // Start after free memory pointer area
            let output_len := 0

            let i := 0 // Input position
            let toggle := 0 // 0 = expecting high nibble, 1 = expecting low nibble
            let hold := 0 // Holds the high nibble

            // Main decode loop
            for {} lt(i, calldatasize()) { i := add(i, 1) } {
                let v := byte(0, calldataload(i))

                let nibble_value := 0
                let is_valid_hex := 0

                // Check for 'a' to 'f' (97-102)
                if and(iszero(lt(v, 97)), iszero(gt(v, 102))) {
                    nibble_value := sub(v, 87)
                    is_valid_hex := 1
                }

                // Check for '0' to '9' (48-57)
                if and(iszero(lt(v, 48)), iszero(gt(v, 57))) {
                    nibble_value := sub(v, 48)
                    is_valid_hex := 1
                }

                // Check for 'A' to 'F' (65-70)
                if and(iszero(lt(v, 65)), iszero(gt(v, 70))) {
                    nibble_value := sub(v, 55)
                    is_valid_hex := 1
                }

                // Check for comment characters ';' (59) or '#' (35)
                if or(eq(v, 59), eq(v, 35)) {
                    // Skip to end of line
                    for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                        let comment_char := byte(0, calldataload(i))

                        // Break on '\r' (13) or '\n' (10)
                        if or(eq(comment_char, 13), eq(comment_char, 10)) { break }
                    }
                }

                // If not a valid hex character, skip (whitespace handling)
                if iszero(is_valid_hex) { continue }

                // Process valid hex nibble
                switch toggle
                case 0 {
                    // High nibble - shift left and store
                    hold := shl(4, nibble_value)
                    toggle := 1
                }
                default {
                    // Low nibble - combine with high nibble and store byte
                    let complete_byte := or(hold, nibble_value)
                    mstore8(add(output_ptr, output_len), complete_byte)
                    output_len := add(output_len, 1)
                    toggle := 0
                }
            }

            // Return the decoded output
            return(output_ptr, output_len)
        }
    }
}
