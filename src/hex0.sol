// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract hex0 {
    bytes11 private immutable datacontractInitcodePrefix;
    
    constructor(bytes11 _datacontractInitcodePrefix) {
        datacontractInitcodePrefix = _datacontractInitcodePrefix;
    }
    
    fallback(bytes calldata input) external returns (bytes memory) {
        uint256 i = 0;
        bool toggle = false;
        uint256 hold = 0;
        bytes memory output = abi.encodePacked(datacontractInitcodePrefix);
        
        while (i < input.length) {
            uint8 c = uint8(input[i]);
            uint256 v = uint256(c);
            
            if (v >= 97 && v <= 102) { // 'a' to 'f'
                hold |= v - 87;
            } else if (v == 59 || v == 35) { // ';' or '#' - comment handling
                // Skip to end of line
                while (true) {
                    i++;
                    if (i >= input.length) break;
                    uint8 nextChar = uint8(input[i]);
                    if (nextChar == 13 || nextChar == 10) { // '\r' or '\n'
                        break;
                    }
                }
                i++;
                continue; // no nibble to output
            } else if (v >= 48 && v <= 57) { // '0' to '9'
                hold |= v - 48;
            } else if (v >= 65 && v <= 70) { // 'A' to 'F'
                hold |= v - 55;
            } else {
                i++;
                continue; // no nibble to output
            }
            
            if (toggle) {
                output = abi.encodePacked(output, uint8(hold));
                hold = 0;
                toggle = false;
            } else {
                hold <<= 4;
                toggle = true;
            }
            i++;
        }
        
        // Return the processed data
	address deployed_address;
        assembly {
		// TODO: salt is the hash of the input
            deployed_address := create2(0, add(output, 0x20), mload(output), 0)
        }
	return abi.encode(deployed_address);
    }
}
