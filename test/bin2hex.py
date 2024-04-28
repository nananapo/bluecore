import sys

def print_usage():
    print(sys.argv[1] )
    print("Usage:", sys.argv[0], "[align(4 or 8)] [filename]")
    exit()

args = sys.argv[1:]
if len(args) != 2:
    print_usage()
if args[0] != "4" and args[0] != "8":
    print_usage()

ALIGN = int(args[0])
FILE_NAME = args[1]

allbytes = []
with open(FILE_NAME, "rb") as f:
    allbytes = f.read()

all = []
for b in allbytes:
    all.append(format(b, '02x'))

all += ["00"] * (ALIGN - len(all) % ALIGN)

aligned = []
for i in range(0, len(all), ALIGN):
    s = ""
    for j in range(ALIGN - 4, -1, -4):
        for k in range(j+3, j-1, -1):
            s += all[i + k]
    aligned.append(s)

print("\n".join(aligned))