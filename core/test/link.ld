OUTPUT_ARCH( "riscv" )
ENTRY(_start)

SECTIONS
{
  . = 0x80000000;
  .text.init : { *(.text.init) }
  .text : { *(.text*) }
  .data : { *(.data*) }
  .bss : {*(.bss*)}
  .stack : {
    . = ALIGN(0x10);
    _stack_top = .;
    . += 4K;
    _stack_bottom = .;
  }
  _end = .;
}
