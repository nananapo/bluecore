#include <iostream>
#include <filesystem>
#include <stdlib.h>
#include <verilated.h>
#include "Vcore_top.h"
#include <verilated_vcd_c.h>

namespace fs = std::filesystem;

extern "C" const char* get_env_value(const char* key) {
    const char* value = getenv(key);
    if (value == nullptr)
        return ""; 
    return value;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);

    // #@@range_begin(arg)
    if (argc < @<b>|3|) {
        std::cout << "Usage: " << argv[0] << " @<b>|ROM_FILE_PATH| RAM_FILE_PATH [CYCLE]" << std::endl;
        return 1;
    }
    // #@@range_end(arg)

    // #@@range_begin(path)
    // メモリの初期値を格納しているファイル名
    @<b>|std::string rom_file_path = argv[1];|
    std::string ram_file_path = argv[@<b>|2|];
    try {
        // 絶対パスに変換する
        @<b>|rom_file_path = fs::absolute(rom_file_path).string();|
        @<b>|ram_file_path = fs::absolute(ram_file_path).string();|
    } catch (const std::exception& e) {
        std::cerr << "Invalid memory file path : " << e.what() << std::endl;
        return 1;
    }
    // #@@range_end(path)

    // シミュレーションを実行するクロックサイクル数
    // #@@range_begin(cycles)
    unsigned long long cycles = 0;
    if (argc >= @<b>|4|) {
        std::string cycles_string = argv[@<b>|3|];
        try {
            cycles = stoull(cycles_string);
        } catch (const std::exception& e) {
            std::cerr << "Invalid number: " << argv[@<b>|3|] << std::endl;
            return 1;
        }
    }
    // #@@range_end(cycles)

    // 環境変数でメモリの初期化用ファイルを指定する
    // #@@range_begin(setenv)
    @<b>|const char* original_env_rom = getenv("ROM_FILE_PATH");|
    const char* original_env_ram = getenv("RAM_FILE_PATH");
    @<b>|setenv("ROM_FILE_PATH", rom_file_path.c_str(), 1);|
    setenv("RAM_FILE_PATH", ram_file_path.c_str(), 1);
    // #@@range_end(setenv)

    // top
    Vcore_top *dut = new Vcore_top();

    // reset
    dut->clk = 0;
    dut->rst = 1;
    dut->eval();
    dut->rst = 0;
    dut->eval();

    // 環境変数を元に戻す
    // #@@range_begin(back)
    @<b>|if (original_env_rom != nullptr){|
    @<b>|    setenv("ROM_FILE_PATH", original_env_rom, 1);|
    @<b>|}|
    if (original_env_ram != nullptr){
        setenv("RAM_FILE_PATH", original_env_ram, 1);
    }
    // #@@range_end(back)

    // trace
    #ifdef TRACE
    Verilated::traceEverOn(true);
    VerilatedVcdC* tfp = new VerilatedVcdC;
    dut->trace(tfp, 100);
    tfp->open("sim.vcd");
    #endif

    // loop
    dut->rst = 1;
    for (long long i=0; !Verilated::gotFinish() && (cycles == 0 || i / 2 < cycles); i++) {
        dut->clk = !dut->clk;
        dut->eval();
        #ifdef TRACE
        tfp->dump((int)i);
        #endif
    }

    dut->final();

    #ifdef TEST_MODE
        return dut->test_success != 1;
    #endif
}
