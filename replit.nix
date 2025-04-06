{ pkgs }: {
  deps = [
    pkgs.lsof
    pkgs.python311
    pkgs.python311Packages.pip
  ];
}
