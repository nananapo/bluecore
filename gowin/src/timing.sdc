//Copyright (C)2014-2024 GOWIN Semiconductor Corporation.
//All rights reserved.
//File Title: Timing Constraints file
//Tool Version: V1.9.9 (64-bit) 
//Created Time: 2024-04-21 05:15:58
create_clock -name clk_in -period 10 -waveform {0 5} [get_ports {clk_in}]
create_clock -name clk -period 10 -waveform {0 5} [get_nets {clk}]
