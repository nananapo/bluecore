#include <iostream>
#include <verilated.h>
#include "Vcore_top.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vcore_top *dut = new Vcore_top();

    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " [cycle]" << std::endl;
        return 1;
    }

    std::string arg2(argv[1]);
    long long loopcount = stoll(arg2);
    loopcount = loopcount * 2;

    dut->clk_in = 0;
    dut->rst_in = 1;
    dut->eval();

    // reset
    dut->rst_in = 0;
    dut->eval();
    dut->rst_in = 1;

    for (int i=0; loopcount == 0 | i < loopcount; i++) {
        dut->clk_in = !dut->clk_in;
        dut->eval();
    }

    dut->final();
}