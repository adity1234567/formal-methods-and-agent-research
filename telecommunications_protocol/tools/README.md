# External tools

## Alloy Analyzer

Download the executable JAR from the
[official AlloyTools 6.2.0 release](https://github.com/AlloyTools/org.alloytools.alloy/releases/tag/v6.2.0).
Save it in this directory with the name `alloy-6.2.0.jar`.

The JAR is an external dependency and is not committed to this repository.
The verification runner expects this exact local path. Java must also be
available on `PATH`.

## Optional: external SAT solvers and proof checker

`scale_verify.py --solver kissat` (or `cadical`) exports each UNSAT-expected
check to CNF with Alloy and decides it with an external solver. `--proof`
additionally checks a DRAT proof with `drat-trim`. See
[the design notes](../scaling_design.md#external-sat-solvers-and-proof-checking).

The runner uses `kissat`, `cadical` and `drat-trim` from `PATH` when present.
Otherwise, on Windows, it runs them inside WSL from
`$HOME/sat-solvers/root/usr/bin` (override with `--sat-bin <linux directory>`).
On Ubuntu under WSL they can be installed without administrator rights:

```shell
mkdir -p ~/sat-solvers/deb && cd ~/sat-solvers/deb
apt-get download kissat cadical drat-trim
for f in *.deb; do dpkg -x "$f" ~/sat-solvers/root; done
~/sat-solvers/root/usr/bin/kissat --version
```

The recorded evidence used the Ubuntu packages kissat 4.0.3-2, cadical 2.1.3-2
and drat-trim 0.0~git20240428.effa1dc-2build1. With root access,
`sudo apt install kissat cadical drat-trim` is equivalent.

## Optional: Z3 for the unbounded obligations

```shell
python -m pip install -r requirements-unbounded.txt
python unbounded_check.py
```
