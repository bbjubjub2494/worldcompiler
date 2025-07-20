contract hex0 {
    fallback() external {
        assembly {
            let toggle
            let hold

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
