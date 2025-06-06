# bluecore

bluecore is 5-stage pipelined ```RV64IMACZicsr_Zifencei_Zicntr``` CPU written in [Veryl](https://github.com/veryl-lang/veryl).  
It supports Sv39.

Do you want to write CPU in Veryl?  
Yes! you can see [instruction](https://cpu.kanataso.net/).

#### riscv-tests
- [x] rv64u(i/m/a/c)-(p/v)-*
- [x] rv64(s/m)i-p-*

### build simulator

require Verilator

```sh
$ cd core
$ make build
$ make sim
# target is objdir/sim
```

### run your program

compile ```test.c```
```sh
$ riscv64-unknown-elf-gcc -nostartfiles -nostdlib -T test/link.ld test.c test/entry.S 
```

convert elf to hex format
```sh
$ riscv64-unknown-elf-objcopy a.out -O binary test.bin
$ python3 test/bin2hex.py 8 test.bin > test.bin.hex
```

run simulator

```sh
$ obj_dir/sim bootrom.hex test.bin.hex
```
