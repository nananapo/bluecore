fileName = "src/decoder.sv"

S = None
with open(fileName, mode="r") as f:
    S = f.readlines()

with open(fileName, mode="w") as f:
    for i in range(len(S)):
        s = S[i]
        s = s.replace("case (", "casez (")
        S[i] = s
        f.write(s)