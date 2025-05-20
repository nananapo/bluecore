#define DEBUG_REG ((volatile unsigned long long*)0x40000000)

void main(void) {
    while (1) {
        unsigned long long c = *DEBUG_REG;
        if (c & (0x01010ULL << 44) == 0) {
            continue;
        }
        c = c & 255;
        *DEBUG_REG = (c + 1) | (0x01010ULL << 44);
    }
}
