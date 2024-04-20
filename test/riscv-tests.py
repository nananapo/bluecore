import sys
import os
import subprocess
import concurrent.futures

TESTS_PATH = "riscv-tests-bin/"
MAKE_COMMAND_VERILATOR = "make -C ../ verilator "
MAX_WORKERS = 1

proc = None

def get_lines(cmd):
    global proc
    proc = subprocess.Popen("exec "+ cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

def test(cmd, filename):
    # run test
    resultFileName = "../test/results/" + filename.replace("/","_") + ".txt"
    cmd = cmd + " > " + resultFileName

    for line in get_lines(cmd):
        continue

    success = False
    for line in get_lines("tail -100 " + resultFileName):
        if "riscv-tests: Success!" in line:
            success = True
            break
    proc.kill()

    if success:
        print("PASS : "+ filename)
    else:
        print("FAIL : "+ filename)
    return (filename, success)



if __name__ == '__main__':
    os.makedirs("../test/results", exist_ok=True)
    results = []
    resultstatus = []
    args = sys.argv[1:]

    while True:
        if len(args) > 0:
            flg = args[0]
            if flg == "-j":
                args = args[1:]
                try:
                    MAX_WORKERS = int(args[0])
                except:
                    print("Usage: -j [num]")
                    exit()
                args = args[1:]
            else:
                break
        else:
            break

    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        processes = []
        for fileName in sorted(os.listdir(TESTS_PATH)):
            if not fileName.endswith(".aligned"):
                continue
            abpath = os.getcwd() + "/" + TESTS_PATH + "/" + fileName

            if len(args) == 0 or fileName.find(args[0]) != -1:
                mcmd = MAKE_COMMAND_VERILATOR
                options = []
                options.append("MEMFILE="+abpath)
                options.append("CYCLE=5000")
                options.append("MDIR="+fileName+"/")
                processes.append(executor.submit(test, mcmd + " " + " ".join(options), fileName))


        for _ in concurrent.futures.as_completed(processes):
            f, s = _.result()
            if s:
                results.append("PASS: " + f)
            else:
                results.append("FAIL: " + f)
            resultstatus.append(s)

    results = sorted(results)

    successCount = str(sum(resultstatus))
    statusText = "Test Result : " + successCount + " / " + str(len(resultstatus))

    with open("results/result.txt", "w", encoding='utf-8') as f:
        f.write(statusText + "\n")
        f.write("\n".join(results))

    print(statusText)

    if sum(resultstatus) != len(resultstatus):
        exit(1)
