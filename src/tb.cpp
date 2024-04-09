#include <iostream>
#include <verilated.h>
#include "Vcore_top.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vcore_top *dut = new Vcore_top();

    dut->clk = 0;
    dut->rst = 1;
    dut->eval();

    int loopcount;
    std::cout << "execute clock(loop=0)?:";
    std::cin >> loopcount;
    loopcount = loopcount * 2;

    // reset
    dut->rst = 0;
    dut->eval();
    dut->rst = 1;

    for (int i=0; loopcount == 0 | i < loopcount; i++) {
        dut->clk = !dut->clk;
        dut->eval();
    }

    dut->final();
}