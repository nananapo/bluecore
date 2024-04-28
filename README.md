# bluecore
[![riscv-tests](https://github.com/nananapo/bluecore/actions/workflows/riscv-tests-verilator.yml/badge.svg)](https://github.com/nananapo/bluecore/actions/workflows/riscv-tests-verilator.yml)

RISC-V Processor written in [Veryl](https://github.com/veryl-lang/veryl).

bluecore is 5-stage in-order core supporting subset of RV32I.  
Veryl version is latest on master branch.  

### build

```sh
$ git clone https://github.com/nananapo/bluecore
$ git submodule init
$ git submodule update
$ make build
```
### run test

- [x] rv32ui-p-*

```sh
$ make verilator MEMFILE=test/riscv-tests-bin/rv32ui-p-add.bin.hex CYCLE=0
...
wdata: 0000000000000001
test: Success
```

RV32I is selected as default. You can change ISA by change config.
https://github.com/nananapo/bluecore/blob/353b16a1e0ecae902610ceb883ae1298682f97ca/core/src/PackageConf.veryl#L1-L2

### synthesize
```synth/gowin/``` directory is GOWIN FPGA Designer project.  
You can synthesize bluecore on TangMega 138K Pro Dock (GW5AST).

Change ```SYNTHESIS_GOWIN=0``` to ```1``` in ```core/src/PackageConf.veryl``` and run ```make build``` before open projects.
