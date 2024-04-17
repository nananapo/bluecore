module memory #(
    // parameter FILEPATH = "",
    parameter DATA_WIDTH = 64,
    parameter ADDR_WIDTH = 16
)(
    input clk,
    input rst,
    output ready,
    input valid,
    input wen,
    input [ADDR_WIDTH-1:0]  addr,
    input [DATA_WIDTH-1:0]  wdata,
    input [DATA_WIDTH/8-1:0] wmask,
    output logic                  rvalid,
    output logic [DATA_WIDTH-1:0] rdata
);

logic [DATA_WIDTH-1:0] mem_data [2**ADDR_WIDTH-1:0];

`ifndef FILEPATH
    initial begin
        $display("FILEPATH not found");
    end
    `error "FILEPATH not found"
    `define FILEPATH ""
`endif

initial begin
    assert(ADDR_WIDTH > 0);
    assert(DATA_WIDTH > 0);
    if (`FILEPATH != "") begin
        $display("FILEPATH: %s", `FILEPATH);
        $readmemh(`FILEPATH, mem_data);
    end
    rdata = 0;
end

typedef enum logic {
    STATE_READY,
    STATE_WRITE
} State;

State state;

logic [ADDR_WIDTH-1:0] addr_saved;
logic [DATA_WIDTH-1:0] wdata_saved;
logic [DATA_WIDTH/8-1:0] wmask_saved;

wire logic [ADDR_WIDTH-1:0] addr_op = state == STATE_READY ? addr : addr_saved;

wire logic [DATA_WIDTH-1:0] wmask_expand;
for (genvar i=0; i<DATA_WIDTH; i++) begin : wm_expand_block
    assign wmask_expand[i] = wmask_saved[i / 8];
end

assign ready = state == STATE_READY;

always @(posedge clk) begin
    if (!rst) begin
        rvalid  <= 0;
        rdata   <= 0;
        state   <= STATE_READY;
    end else begin
        if (state == STATE_READY) begin
            if (valid) begin
                rvalid  <= !wen;
                rdata   <= mem_data[addr_op];

                addr_saved  <= addr;
                wdata_saved <= wdata;
                wmask_saved <= wmask;

                if (wen) begin
                    state <= STATE_WRITE;
                end
            end else begin
                rvalid <= 0;
            end
        end else if (state == STATE_WRITE) begin
            rvalid <= 1;
            mem_data[addr_op] <= wdata_saved & wmask_expand | rdata & ~wmask_expand;
            state <= STATE_READY;
        end
    end
end

endmodule
