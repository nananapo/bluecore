
CASEX_LINT_OFF = "/* verilator lint_off CASEX */\n"
CASEX_LINT_ON  = "/* verilator lint_on CASEX */\n"
CASEX = "casex"

fileName = "src/decoder.sv"


S = None
with open(fileName, mode="r") as f:
    S = f.readlines()

with open(fileName, mode="w") as f:
    f.write(CASEX_LINT_OFF)
    for i in range(len(S)):
        s = S[i]
        s = s.replace("case (", "casex (")
        S[i] = s
        f.write(s)
    f.write(CASEX_LINT_ON)
