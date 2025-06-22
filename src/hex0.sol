// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract hex0 {
    bytes11 private immutable datacontractInitcodePrefix;
    
    constructor(bytes11 _datacontractInitcodePrefix) {
        datacontractInitcodePrefix = _datacontractInitcodePrefix;
    }
    
    fallback(bytes calldata input) external returns (bytes memory output) {
        uint256 i = 0;
        bool toggle = false;
        uint256 hold = 0;
        
        while (i < input.length) {
            uint8 v = uint8(input[i]);
            i++;
            
            if (v >= 97 && v <= 102) { // 'a' to 'f'
                hold |= v - 87;
            } else if (v >= 48 && v <= 57) { // '0' to '9'
                hold |= v - 48;
            } else if (v >= 65 && v <= 70) { // 'A' to 'F'
                hold |= v - 55;
            } else if (v == 59 || v == 35) { // ';' or '#' - comment handling
                // Skip to end of line
                while (i < input.length) {
                    v = uint8(input[i]);
		    i++;
                    if (v == 13 || v == 10) { // '\r' or '\n'
                        break;
                    }
                }
                continue; // no nibble to output
            } else {
                continue; // no nibble to output
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
}
