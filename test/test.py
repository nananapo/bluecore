import argparse
import os
import subprocess
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument("project_dir", help="path to bluecore root directory")
parser.add_argument("dir", help="directory includes test")
parser.add_argument("files", nargs='*', help="test hex file names")
parser.add_argument("-r", "--recursive", action='store_true', help="search file recursively")
parser.add_argument("-e", "--extension", default="hex", help="test file extension")
parser.add_argument("-j", "--jobs", type=int, default=1, help="run N tests at once")
parser.add_argument("-o", "--output_dir", default="results", help="result output directory")
parser.add_argument("-t", "--time_limit", type=float, default=10, help="limit of execution time. set 0 to nolimit")
parser.add_argument("--test_exit_addr", default="'h1000", help="exit address on test")
parser.add_argument("--test_wdata_succ", type=int, default=1, help="write value on test success")
args = parser.parse_args()

EXEFILE_MAGIC = "executable file: "
MAKE_CMD_VERILATOR = "make -C " + args.project_dir+ " verilator "

def read_lines(proc):
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

def create_cmd(cmd, options):
    return "exec " + cmd + " " + " ".join(options)

def test(fileName):
    resultFilePath = os.path.join(args.output_dir, fileName.replace(os.sep, "_") + ".txt")
    mdir = fileName.replace(os.sep, "_")

    makecmd = MAKE_CMD_VERILATOR

    options = []
    options.append("MEMFILE="+fileName)
    options.append("MDIR="+mdir+"/")
    params = []
    params.append("-DENV_TEST")
    params.append("-DTEST_EXIT_ADDR="+args.test_exit_addr)
    params.append("-DTEST_WDATA_SUCCESS="+str(args.test_wdata_succ))
    options.append("OPTION=\"" + " ".join(map(lambda x:x.replace("\"", "\\\"").replace("\'", "\\\'") ,params)) + "\"")

    with open(resultFilePath, "w") as f:
        run_command = None
        # コンパイル
        p = subprocess.Popen(create_cmd(makecmd, options), shell=True, stdout=subprocess.PIPE)
        try:
            for line in read_lines(p):
                line = line.decode()
                f.write(line)
                if line.startswith(EXEFILE_MAGIC):
                    run_command = line[len(EXEFILE_MAGIC):-1]
            p.wait(None if args.time_limit == 0 else args.time_limit)
        except: pass
        finally:
            p.kill()
        # 実行する
        no = f.fileno()
        if p.returncode == 0 and run_command is not None:
            p = subprocess.Popen(create_cmd(run_command, ["0"]), shell=True, stdout=no, stderr=no)
            try:
                p.wait(None if args.time_limit == 0 else args.time_limit)
            except: pass
            finally:
                p.kill()

    success = False
    # 結果の最後の100行以内にSuccessが含まれているかをチェックする    
    try:
        p = subprocess.Popen(create_cmd("tail", ["-100", resultFilePath]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in read_lines(p):
            if "test: Success" in line:
                success = True
                break
    except: pass
    finally:
        p.kill()

    print(("PASS" if success else "FAIL") + " : "+ fileName)
    return (fileName, success)

def dir_walk(dir):
    for entry in os.scandir(dir):
        if entry.is_dir():
            if args.recursive:
                for e in dir_walk(entry.path):
                    yield e
            continue
        if entry.is_file():
            if not entry.name.endswith(args.extension):
                continue
            if len(args.files) == 0:
                yield entry.path
            for f in args.files:
                if entry.name.find(f) != -1:
                    yield entry.path
                    break

if __name__ == '__main__':
    os.makedirs(args.output_dir, exist_ok=True)

    res_strs = []
    res_statuses = []
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as executor:
        processes = []
        for hexpath in dir_walk(args.dir):
            processes.append(executor.submit(test, os.path.abspath(hexpath)))
        for _ in concurrent.futures.as_completed(processes):
            f, s = _.result()
            res_strs.append(("PASS" if s else "FAIL") + " : " + f)
            res_statuses.append(s)

    res_strs = sorted(res_strs)

    successCount = str(sum(res_statuses))
    statusText = "Test Result : " + successCount + " / " + str(len(res_statuses))

    with open(os.path.join(args.output_dir, "result.txt"), "w", encoding='utf-8') as f:
        f.write(statusText + "\n")
        f.write("\n".join(res_strs))

    print(statusText)

    if sum(res_statuses) != len(res_statuses):
        exit(1)