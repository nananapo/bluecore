#include <iostream>
#include <filesystem>
#include <stdlib.h>
#include <verilated.h>
#include <fcntl.h>
#include <termios.h>
#include <signal.h>
#include "Vcore_top.h"
#include <verilated_vcd_c.h>

namespace fs = std::filesystem;

extern "C" const char* get_env_value(const char* key) {
    const char* value = getenv(key);
    if (value == nullptr)
        return ""; 
    return value;
}

extern "C" const unsigned long long get_input_dpic() {
    unsigned char c = 0;
    ssize_t bytes_read = read(STDIN_FILENO, &c, 1);

    if (bytes_read == 1) {
        return static_cast<unsigned long long>(c) | (0x01010ULL << 44);
    }
    return 0;
}

struct termios old_setting;

void restore_termios_setting(void) {
    tcsetattr(STDIN_FILENO, TCSANOW, &old_setting);
}

void sighandler(int signum) {
    restore_termios_setting();
    exit(signum);
}

void set_nonblocking(void) {
    struct termios new_setting;

    if (tcgetattr(STDIN_FILENO, &old_setting) == -1) {
        perror("tcgetattr");
        return;
    }
    new_setting = old_setting;
    new_setting.c_lflag &= ~(ICANON | ECHO);
    if (tcsetattr(STDIN_FILENO, TCSANOW, &new_setting) == -1) {
        perror("tcsetattr");
        return;
    }
    signal(SIGINT, sighandler);
    signal(SIGTERM, sighandler);
    signal(SIGQUIT, sighandler);
    atexit(restore_termios_setting);

    int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    if (flags == -1) {
        perror("fcntl(F_GETFL)");
        return;
    }
    if (fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK) == -1) {
        perror("fcntl(F_SETFL)");
        return;
    }
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);

    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " ROM_FILE_PATH RAM_FILE_PATH [CYCLE]" << std::endl;
        return 1;
    }

    #ifdef ENABLE_DEBUG_INPUT
        set_nonblocking();
    #endif

    // メモリの初期値を格納しているファイル名
    std::string rom_file_path = argv[1];
    std::string ram_file_path = argv[2];
    try {
        // 絶対パスに変換する
        rom_file_path = fs::absolute(rom_file_path).string();
        ram_file_path = fs::absolute(ram_file_path).string();
    } catch (const std::exception& e) {
        std::cerr << "Invalid memory file path : " << e.what() << std::endl;
        return 1;
    }

    // シミュレーションを実行するクロックサイクル数
    unsigned long long cycles = 0;
    if (argc >= 4) {
        std::string cycles_string = argv[3];
        try {
            cycles = stoull(cycles_string);
        } catch (const std::exception& e) {
            std::cerr << "Invalid number: " << argv[3] << std::endl;
            return 1;
        }
    }

    // 環境変数でメモリの初期化用ファイルを指定する
    const char* original_env_rom = getenv("ROM_FILE_PATH");
    const char* original_env_ram = getenv("RAM_FILE_PATH");
    setenv("ROM_FILE_PATH", rom_file_path.c_str(), 1);
    setenv("RAM_FILE_PATH", ram_file_path.c_str(), 1);

    // デバッグ用の入出力デバイスのアドレスを取得する
    const char* dbg_addr_c = getenv("DBG_ADDR");
    const unsigned long long DBG_ADDR = dbg_addr_c == nullptr ? 0 : std::strtoull(dbg_addr_c, nullptr, 0);

    // top
    Vcore_top *dut = new Vcore_top();
    dut->MMAP_DBG_ADDR = DBG_ADDR;

    // reset
    dut->clk = 0;
    dut->rst = 1;
    dut->eval();
    dut->rst = 0;
    dut->eval();

    // 環境変数を元に戻す
    if (original_env_rom != nullptr){
        setenv("ROM_FILE_PATH", original_env_rom, 1);
    }
    if (original_env_ram != nullptr){
        setenv("RAM_FILE_PATH", original_env_ram, 1);
    }

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
