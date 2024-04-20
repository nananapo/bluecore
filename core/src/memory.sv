/// メモリモジュール
///
/// ready = 1のときに命令を受容する
/// valid = 1になったクロックの命令を受容する
/// valid = 1になった次以降のクロックで結果を出力する
/// rvalid = 1のクロックでのみ結果を出力する
/// rvalid = 0のとき、前クロックでの結果は保持しない
module memory #(
    parameter  int unsigned DATA_WIDTH  = 0             ,
    parameter  int unsigned ADDR_WIDTH  = 0             ,
    parameter  string       FILE_PATH   = ""            ,
    localparam int unsigned WMASK_WIDTH = DATA_WIDTH / 8
) (
    input  logic                   clk   ,
    input  logic                   rst   ,
    output logic                   ready ,
    input  logic                   valid ,
    input  logic                   wen   ,
    input  logic [ADDR_WIDTH-1:0]  addr  ,
    input  logic [DATA_WIDTH-1:0]  wdata ,
    input  logic [WMASK_WIDTH-1:0] wmask ,
    output logic                   rvalid,
    output logic [DATA_WIDTH-1:0]  rdata 
);

    logic [DATA_WIDTH-1:0] mem_data [2 ** ADDR_WIDTH-1:0];

    initial begin
        // パラメータの確認
        if (ADDR_WIDTH == 0) begin
            $fatal("ADDR_WIDTH == 0");
        end
        if (DATA_WIDTH == 0) begin
            $fatal("DATA_WIDTH == 0");

        end
        if (FILE_PATH != "") begin
            // ファイルのデータを初期値として書き込む
            $display ("FILE_PATH: %s", FILE_PATH);
            $readmemh(FILE_PATH, mem_data);
        end
    end

    // メモリのステート
    typedef enum logic {
        State_Ready,
        State_Write
    } State;
    State state;

    // 書き込み命令のデータ保持用レジスタ
    logic [ADDR_WIDTH-1:0]  addr_save ;
    logic [DATA_WIDTH-1:0]  wdata_save;
    logic [WMASK_WIDTH-1:0] wmask_save;

    // データ幅に合わせたマスクの生成
    logic [DATA_WIDTH-1:0] wmask_expand;
    for (genvar i = 0; i < DATA_WIDTH; i++) begin :wm_expand_block
        always_comb wmask_expand[i] = wmask_save[i / 8];
    end

    // アクセスするアドレス
    logic [ADDR_WIDTH-1:0] access_addr;
    always_comb access_addr = ((state == State_Ready) ? (
        addr
    ) : (
        addr_save
    ));

    always_comb ready = state == State_Ready;

    always_ff @ (posedge clk, negedge rst) begin
        if (!rst) begin
            rvalid     <= 0;
            rdata      <= 0;
            state      <= State_Ready;
            addr_save  <= 'x;
            wdata_save <= 'x;
            wmask_save <= 'x;
        end else begin
            if ((state == State_Ready)) begin
                if ((valid)) begin
                    rvalid <= !wen;
                    rdata  <= mem_data[access_addr];
                    // 書き込み命令用にデータを保存
                    addr_save  <= addr;
                    wdata_save <= wdata;
                    wmask_save <= wmask;
                    // 書き込み命令の場合はステートを移動
                    if ((wen)) begin
                        state <= State_Write;
                    end
                end else begin
                    rvalid <= 0;
                end
            end else if ((state == State_Write)) begin
                // READYステートに戻る
                state  <= State_Ready;
                rvalid <= 1;
                // マスクした値の書き込み
                mem_data[access_addr] <= wdata_save & wmask_expand | rdata & ~wmask_expand;
            end
        end
    end
endmodule
