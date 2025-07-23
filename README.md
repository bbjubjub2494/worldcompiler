# The World Compiler

An experiment that leverages blockchains to verifiably compile software.

```
packages/
  ├── computation-registry           <-- Using blockchain state as proof of the result of a computation
  ├── deterministic-deployment-proxy <-- Python library for Arachnid's Deterministic DeploymentProxy
  ├── erc7744                        <-- Python library for ERC-7744: Code Index
  ├── erc7955                        <-- Python library for ERC-7955: Permissionless Create2
  ├── languages                      <-- Python implementations of minimalist programming languages
  ├── seeds                          <-- EVM bootstrapping implementations of minimalist programming languages
  └── util                           <-- Utilities
```

In the ideal end state, users can receive compiled programs along with their source code and some additional data, and use a non fully reexecuting light client to check that the compilation was performed onchain and that the results match. This relies on the Computation Registry as a way to structure the onchain data, and on zk-EVMs or other forms of verifiable computation.

[ZKBootstrap](https://github.com/bbjubjub2494/zkbootstrap) is an earlier iteration of the concept, which turned out to re-invent parts of what the EVM already abstracts over.

Disclaimer: basically nothing works right now
