import sys

args = sys.argv[1:]
if len(args) == 0:
    print("Usage:", sys.argv[0], " [filename]")
    exit()

FILE_NAME = args[0]

allbytes = []
with open(FILE_NAME, "rb") as f:
    allbytes = f.read()

all = []
for b in allbytes:
    all.append(format(b, '02x'))

ALIGN = 8
all += ["00"] * (ALIGN - len(all) % ALIGN)

aligned = []
for i in range(0, len(all), ALIGN):
    s = ""
    for j in range(ALIGN - 4, -1, -4):
        for k in range(j+3, j-1, -1):
            s += all[i + k]
    aligned.append(s)

print("\n".join(aligned))