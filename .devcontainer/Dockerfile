FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

# Install dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    autoconf \
    automake \
    autotools-dev \
    curl \
    python3 \
    python3-pip \
    python3-tomli \
    libmpc-dev \
    libmpfr-dev \
    libgmp-dev \
    gawk \
    build-essential \
    bison \
    flex \
    texinfo \
    gperf \
    libtool \
    patchutils \
    bc \
    zlib1g-dev \
    libexpat-dev \
    ninja-build \
    git \
    cmake \
    libglib2.0-dev \
    libslirp-dev \
    device-tree-compiler

# riscv-gnu-toolchain (RV32I)
RUN git clone https://github.com/riscv/riscv-gnu-toolchain toolchain-rv32i \
    && cd toolchain-rv32i \
    && ./configure --prefix=/usr/local/riscv32 --with-arch=rv32gc \
    && make -j$(nproc)

# riscv-gnu-toolchain (RV64I)
RUN git clone https://github.com/riscv/riscv-gnu-toolchain toolchain-rv64i \
    && cd toolchain-rv64i \
    && ./configure --prefix=/usr/local/riscv64 --with-arch=rv64gc \
    && make -j$(nproc)

# build riscv-pk for RV32I
RUN export PATH="/usr/local/riscv32/bin:$PATH" \
    && git clone https://github.com/riscv-software-src/riscv-pk.git riscv-pk-rv32 \
    && cd riscv-pk-rv32 \
    && mkdir build && cd build \
    && ../configure --prefix=/usr/local/riscv32 --host=riscv32-unknown-elf \
    && make -j$(nproc) \
    && make install

# build riscv-pk for RV64I
RUN export PATH="/usr/local/riscv64/bin:$PATH" \
    && git clone https://github.com/riscv-software-src/riscv-pk.git riscv-pk-rv64 \
    && cd riscv-pk-rv64 \
    && mkdir build && cd build \
    && ../configure --prefix=/usr/local/riscv64 --host=riscv64-unknown-elf \
    && make -j$(nproc) \
    && make install

# build riscv-isa-sim for RV32I
RUN export PATH="/usr/local/riscv32/bin:$PATH" \
    && git clone https://github.com/riscv-software-src/riscv-isa-sim.git riscv-isa-sim-rv32 \
    && cd riscv-isa-sim-rv32 \
    && mkdir build && cd build \
    && ../configure --prefix=/usr/local/riscv32 --with-target=riscv32-unknown-elf \
    && make -j $(nproc) \
    && make install

# build riscv-isa-sim for RV64I
RUN export PATH="/usr/local/riscv64/bin:$PATH" \
    && git clone https://github.com/riscv-software-src/riscv-isa-sim.git riscv-isa-sim-rv64 \
    && cd riscv-isa-sim-rv64 \
    && mkdir build && cd build \
    && ../configure --prefix=/usr/local/riscv64 --with-target=riscv64-unknown-elf \
    && make -j $(nproc) \
    && make install

# create setenv32 file
RUN echo 'export PATH=/usr/local/riscv32/bin:$PATH' >> /home/vscode/setenv32.sh \
    && echo 'export RISCV=/usr/local/riscv32' >> /home/vscode/setenv32.sh

# create setenv64 file
RUN echo 'export PATH=/usr/local/riscv64/bin:$PATH' >> /home/vscode/setenv64.sh \
    && echo 'export RISCV=/usr/local/riscv64' >> /home/vscode/setenv64.sh

# install verilator
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends help2man perl g++ ccache
RUN git clone https://github.com/verilator/verilator \
    && cd verilator \
    && git checkout v5.042 \
    && git clone https://github.com/westes/flex .flex \
    && cd .flex \
    && git checkout v2.6.4 \
    && cd .. \
    && cp .flex/src/FlexLexer.h include/FlexLexer.h \
    && cp .flex/src/FlexLexer.h FlexLexer.h
RUN cd verilator \
    && autoconf \
    && ./configure \
    && make -j 4 \
    && make install

# install sail
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends opam z3 pkg-config
RUN opam init -y \
    && opam switch create 5.1.0 \
    && opam install -y sail

# install sail-riscv
RUN eval $(opam env) \
    && git clone https://github.com/riscv/sail-riscv sail-riscv \
    && cd sail-riscv \
    && git checkout 0.9 \
    && ./build_simulators.sh
RUN cd sail-riscv \
    && echo '#!/bin/sh\nexec '$(pwd)'/build/c_emulator/sail_riscv_sim --config /sail-riscv/build/config/rv32d_v256_e32.json "$@"' \
    > /usr/local/riscv32/bin/riscv_sim_RV32 \
    && chmod +x /usr/local/riscv32/bin/riscv_sim_RV32
RUN cd sail-riscv \
    && echo '#!/bin/sh\nexec '$(pwd)'/build/c_emulator/sail_riscv_sim --config /sail-riscv/build/config/rv64d_v256_e64.json "$@"' \
    > /usr/local/riscv64/bin/riscv_sim_RV64 \
    && chmod +x /usr/local/riscv64/bin/riscv_sim_RV64

# Install Rust
USER vscode
RUN RUSTUP_HOME=/home/vscode/.rustup \
    CARGO_HOME=/home/vscode/.cargo \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable

# install verylup and veryl
RUN . "$HOME/.cargo/env" \
    && cargo install verylup \
    && verylup setup
RUN . "$HOME/.cargo/env" \
    && verylup install nightly \
    && verylup default nightly

# install riscof
RUN pip3 install riscof

# install pyelftools
RUN pip3 install pyelftools