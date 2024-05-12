package svconfig;
    // メモリの初期値
    `ifndef MEMORY_INITIAL_FILE
        `define MEMORY_INITIAL_FILE ""
    `endif
    localparam MEMORY_INITIAL_FILE = `MEMORY_INITIAL_FILE;

    // テストモードかどうか
    `ifdef ENV_TEST
        localparam ENV_TEST = 1;
    `else
        localparam ENV_TEST = 0;
    `endif

    // テストモードの時、結果を書き込むアドレス
    `ifndef TEST_EXIT_ADDR
        `define TEST_EXIT_ADDR 'h1000
    `endif
    localparam TEST_EXIT_ADDR = `TEST_EXIT_ADDR;

    // テストモードの時、結果が成功の時に書き込まれる値
    `ifndef TEST_WDATA_SUCCESS
        `define TEST_WDATA_SUCCESS 1
    `endif
    localparam TEST_WDATA_SUCCESS = `TEST_WDATA_SUCCESS;
endpackage
