{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";

  # Load the blueprint
  outputs = inputs: let
    systems = [
      "x86_64-linux"
      "aarch64-linux"
      "x86_64-darwin"
      "aarch64-darwin"
    ];
  in {
    devShells = inputs.nixpkgs.lib.genAttrs systems (system:
      with inputs.nixpkgs.legacyPackages.${system}; {
        default = mkShell {packages = [
          mescc-tools # hex2, M1
          solc # Solidity compiler
        ];
      };
      });
    formatter =
      inputs.nixpkgs.lib.genAttrs systems (system:
        inputs.nixpkgs.legacyPackages.${system}.alejandra);
  };
}
