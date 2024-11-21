module core_top_v #(
    parameter MEMORY_FILEPATH = ""
) (
    input wire          clk,
    input wire          rst,
    output wire [3:0]   led
);
    core_top_pynq_z1 #(
        .MEMORY_FILEPATH(MEMORY_FILEPATH)
    ) t (
        .clk(clk),
        .rst(rst),
        .led(led)
    );
endmodule