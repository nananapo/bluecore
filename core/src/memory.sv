module memory #(
    // parameter FILEPATH = "",
    parameter DATA_WIDTH = 64,
    parameter ADDR_WIDTH = 16
)(
    input clk,
    input rst,
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

wire logic [DATA_WIDTH-1:0] wmask_expand;
for (genvar i=0; i<DATA_WIDTH; i++) begin : wm_expand_block
    assign wmask_expand[i] = wmask[i / 8];
end

always @(posedge clk) begin
    if (!rst) begin
        rvalid  <= 0;
    end else if (valid) begin
        rvalid  <= 1;
        rdata   <= mem_data[addr];
        if (wen)
            mem_data[addr] <=   wdata & wmask_expand |
                                mem_data[addr] & ~wmask_expand;
    end else begin
        rvalid <= 0;
    end
end

endmodule
