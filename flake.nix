{
  description = "Python PDF Converter";

  inputs = {
    nixpkgs.url = "github:DerDennisOP/nixpkgs/comp";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        py = pkgs.python3.override {
          packageOverrides = python-final: python-prev: {
            django = python-final.django_4;
          };
        };
        pythonEnv = py.withPackages (ps: with ps; [
          django
          djangorestframework
          pypdf
	  pdfminer-six
        ]);
      in
      {
        devShell = with pkgs; mkShell {
          packages = [
            pythonEnv
          ];
        };
      }
    );
}
