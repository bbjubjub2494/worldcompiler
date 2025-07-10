# Reference Parsers for EthBootstrap

This package contains Python implementations of the languages used in the EthBootstrap project.
These languages are minimalistic and generic, designed to run inside of smart contracts cheaply and support expressing both EVM and off-chain programs.
They are based on [the stage0 languages by Jeremiah Orians](https://bootstrapping.miraheze.org/wiki/Stage0) and are highly compatible with them.

## Hex0

Hex0 is simply commented hexadecimal.
It is used to implement the other two languages, so that we do not need to trust an external compiler.
Our version is intended to be identical to the original hex0.


## Hex2

Hex2 is hex0 with the addition of alphanumeric labels that can be used to compute absolute and relative jumps.
This makes it powerful enough to act as the linker in the EthBootstrap compiler pipeline.
Compared to the original hex2, we added a syntax for absolute, 1-byte jumps, which is very useful in the EVM since space comes at a premium.

## M1

M1 is a simple macro language that works as a universal assembler.
It allows defining shorthands for instructions in-band, which lets us write programs in a more human-readable way.
If fed with different macro definitions, it can be used to compile to different instruction sets.
It outputs hex2 code, which can then be passed to hex2 for further processing.

In addition to the original features in M1, we intend to add 3 EVM-specific built-in macros:
- `INCLUDE`, which can fetch content from the Ethereum contract trie in a content-addressable way;
- `KECCAK256`, which can compute Keccak-256 hashes at compile time, and
- `4BYTE`, which can produce 4-byte function selectors at compile time.
