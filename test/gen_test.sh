find riscv-tests-bin -type f ! -name "*\.*" -exec sh -c "riscv32-unknown-elf-objcopy -O binary {} {}.bin" \; && find riscv-tests-bin -type f ! -name "*\.*" -exec sh -c "python3 bin2hex.py {}.bin > {}.bin.aligned" \;