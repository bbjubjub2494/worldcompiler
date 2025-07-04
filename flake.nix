{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";

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
          (mescc-tools.overrideAttrs { # hex2, M1
            patches = [
              (fetchpatch {
                url = "https://github.com/bbjubjub2494/mescc-tools/commit/e5658f211d1dbcbfcd173cf397ebc08fa89d150b.patch";
                hash = "sha256-lecU4ozYH8aP/GDwJrj6HCnKaWZsaZrBKjLuu40bMaw=";
              })
            ];
          })
          solc # Solidity compiler
        ];
      };
      });
    formatter =
      inputs.nixpkgs.lib.genAttrs systems (system:
        inputs.nixpkgs.legacyPackages.${system}.alejandra);
  };
}
