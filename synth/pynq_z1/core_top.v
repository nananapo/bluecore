module core_top #(
    parameter string MEMORY_FILEPATH = ""
) (
    input wire          clk,
    input wire          rst,
    output wire [3:0]   led
);
    top_pynq_z1 t #(
        .MEMORY_FILEPATH(MEMORY_FILEPATH)
    ) (
        .clk(clk),
        .rst(rst),
        .led(led)
    );
endmodule