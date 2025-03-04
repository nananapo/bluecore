## build/run your own C program

compile test.c
```sh
$ riscv64-unknown-elf-gcc -nostartfiles -nostdlib -T link.ld test.c entry.S 
```

convert elf to hex format
```sh
$ riscv64-unknown-elf-objcopy a.out -O binary test.bin
$ python3 bin2hex.py 8 test.bin > test.bin.hex
```
