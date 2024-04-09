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
    output logic                  rvalid,
    output logic [DATA_WIDTH-1:0] rdata
);

logic [DATA_WIDTH-1:0] mem [2**ADDR_WIDTH-1:0];

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
        $readmemh(`FILEPATH, mem);
    end
    rdata = 0;
end

always @(posedge clk) begin
    if (!rst) begin
        rvalid  <= 0;
    end else if (valid) begin
        rvalid  <= 1;
        rdata   <= mem[addr];
        if (wen)
            mem[addr] <= wdata;
    end else begin
        rvalid <= 0;
    end
end

endmodule
