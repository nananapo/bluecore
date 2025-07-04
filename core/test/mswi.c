#define MSIP0 ((volatile unsigned int *)0x2000000)
#define DEBUG_REG ((volatile unsigned long long*)0x40000000)
#define MIE_MSIE (1 << 3)
#define MSTATUS_MIE (1 << 3)

void interrupt_handler(void);

void w_mtvec(unsigned long long x) {
    asm volatile("csrw mtvec, %0" : : "r" (x));
}

void w_mie(unsigned long long x) {
    asm volatile("csrw mie, %0" : : "r" (x));
}

void w_mstatus(unsigned long long x) {
    asm volatile("csrw mstatus, %0" : : "r" (x));
}

void main(void) {
    w_mtvec((unsigned long long)interrupt_handler);
    w_mie(MIE_MSIE);
    w_mstatus(MSTATUS_MIE);
    *MSIP0 = 1;
    while (1) *DEBUG_REG = 3; // fail
}

void interrupt_handler(void) {
    *DEBUG_REG = 1; // success
}
