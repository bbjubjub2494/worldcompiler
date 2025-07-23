// Prototype implementation of the hex2 bootstrap parser.
// The goal is to make it reasonably optimized, then rewrite it in hex0.

contract hex2 {
    fallback() external {
        assembly {
            let nibble_count
            let toggle
            let hold

            let dirty := tload(0)
            tstore(0, 1)
            if dirty { revert(hold, toggle) } // reuse known zero slots

            for { let i := 0 } lt(i, calldatasize()) { i := add(i, 1) } {
                let c := byte(0, calldataload(i))
                switch or(lt(c, 0x30), gt(c, 0x39))
                case 0 {}
                default {
                    switch or(lt(c, 0x41), gt(c, 0x46))
                    case 0 {}
                    default {
                        switch or(lt(c, 0x61), gt(c, 0x66))
                        case 0 {}
                        default {
                            if eq(c, 0x3a) {
                                // ':' introduces a label
                                let start := add(i, 1)
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    let c2 := byte(0, calldataload(i))
                                    if and(or(lt(c2, 0x41), gt(c2, 0x5a)), or(lt(c2, 0x61), gt(c2, 0x7a))) { break }
                                }
                                let len := sub(i, start)
                                calldatacopy(0, start, len)
                                let hash := keccak256(0, len)
                                tstore(hash, div(nibble_count, 2))
                                i := sub(i, 1)
                            }
                            if eq(c, 0x2b) {
                                // '+' introduces a 1-byte pointer
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    let c2 := byte(0, calldataload(i))
                                    if and(or(lt(c2, 0x41), gt(c2, 0x5a)), or(lt(c2, 0x61), gt(c2, 0x7a))) { break }
                                }
                                nibble_count := add(nibble_count, 2)
                                i := sub(i, 1)
                            }
                            if or(eq(c, 0x23), eq(c, 0x3b)) {
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    if eq(byte(0, calldataload(i)), 0x0a) { break }
                                }
                            }
                            continue
                        }
                    }
                }
                nibble_count := add(nibble_count, 1)
            }
            let j := 0
            for { let i := 0 } lt(i, calldatasize()) { i := add(i, 1) } {
                let c := byte(0, calldataload(i))
                let n
                switch or(lt(c, 0x30), gt(c, 0x39))
                case 0 { n := sub(c, 0x30) }
                default {
                    switch or(lt(c, 0x41), gt(c, 0x46))
                    case 0 { n := sub(c, 0x37) }
                    default {
                        switch or(lt(c, 0x61), gt(c, 0x66))
                        case 0 { n := sub(c, 0x57) }
                        default {
                            if eq(c, 0x3a) {
                                // ':' introduces a label
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    let c2 := byte(0, calldataload(i))
                                    if and(or(lt(c2, 0x41), gt(c2, 0x5a)), or(lt(c2, 0x61), gt(c2, 0x7a))) { break }
                                }
                                // do nothing
                                i := sub(i, 1)
                            }
                            if eq(c, 0x2b) {
                                // '+' introduces a 1-byte pointer
                                let start := add(i, 1)
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    let c2 := byte(0, calldataload(i))
                                    if and(or(lt(c2, 0x41), gt(c2, 0x5a)), or(lt(c2, 0x61), gt(c2, 0x7a))) { break }
                                }
                                let len := sub(i, start)
                                calldatacopy(j, start, len)
                                let hash := keccak256(j, len)
                                mstore8(j, tload(hash))
                                j := add(j, 1)
                                i := sub(i, 1)
                            }
                            if or(eq(c, 0x23), eq(c, 0x3b)) {
                                for { i := add(i, 1) } lt(i, calldatasize()) { i := add(i, 1) } {
                                    if eq(byte(0, calldataload(i)), 0x0a) { break }
                                }
                            }
                            continue
                        }
                    }
                }
                switch toggle
                case 0 { hold := shl(4, n) }
                default {
                    mstore8(j, or(hold, n))
                    j := add(j, 1)
                }
                toggle := iszero(toggle)
            }
            return(0, j)
        }
    }
}
