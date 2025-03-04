#define DEBUG_REG ((volatile unsigned long long*)0x40000000)

void main(void) {
    int strlen = 13;
    unsigned char str[13];

    str[0]  = 'H';
    str[1]  = 'e';
    str[2]  = 'l';
    str[3]  = 'l';
    str[4]  = 'o';
    str[5]  = ',';
    str[6]  = 'w';
    str[7]  = 'o';
    str[8]  = 'r';
    str[9]  = 'l';
    str[10] = 'd';
    str[11] = '!';
    str[12] = '\n';

    for (int i = 0; i < strlen; i++) {
        unsigned long long c = str[i];
        *DEBUG_REG = c | (0x01010ULL << 44);
    }
    *DEBUG_REG = 1;
}
