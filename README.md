# bluecore
RISC-V Processor written in [Veryl](https://github.com/veryl-lang/veryl).

```
Veryl version : at 794f33d686aad5fe2261a1d037ee991fcd6b2fb1
```
bluecore is 5-stage in-order core supporting subset of RV[32|64]I.

### build
change this line in core/Makefile
https://github.com/nananapo/bluecore/blob/b7ad7a1bb11bb994e0a5f929a3e81def2b54ae18/core/Makefile#L1

```sh
$ make build
```
### run test
```sh
$ make verilator MEMFILE=test/riscv-tests/rv32ui-p-add.bin.aligned CYCLE=0
...
wdata: 0000000000000001
riscv-tests: Success!
```

RV32I is selected as default. You can change ISA by change config.
https://github.com/nananapo/bluecore/blob/main/core/src/PackageConf.veryl#L1-L2

### synthesize
```gowin/``` directory is GOWIN FPGA Designer project.  
You can synthesize bluecore on TangMega 138K Pro Dock (GW5AST).