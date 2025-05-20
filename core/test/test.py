import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("sim_path", help="path to simlator")
parser.add_argument("dir", help="directory includes test")
parser.add_argument("files", nargs='*', help="test hex file names")
parser.add_argument("-r", "--recursive", action='store_true', help="search file recursively")
parser.add_argument("-e", "--extension", default="hex", help="test file extension")
parser.add_argument("-o", "--output_dir", default="results", help="result output directory")
parser.add_argument("-t", "--time_limit", type=float, default=10, help="limit of execution time. set 0 to nolimit")
#@range_begin(arg)
parser.add_argument("--rom", default="bootrom.hex", help="hex file of rom")
#@range_end(arg)
args = parser.parse_args()

# run test
#@range_begin(test)
def test(@<b>|romhex, |file_name):
    result_file_path = os.path.join(args.output_dir, file_name.replace(os.sep, "_") + ".txt")
    cmd = @<b>|f"{args.sim_path} {romhex} {file_name} 0"|
    success = False
#@range_end(test)
    with open(result_file_path, "w") as f:
        no = f.fileno()
        p = subprocess.Popen("exec " + cmd, shell=True, stdout=no, stderr=no)
        try:
            p.wait(None if args.time_limit == 0 else args.time_limit)
            success = p.returncode == 0
        except: pass
        finally:
            p.terminate()
            p.kill()
    print(("PASS" if success else "FAIL") + " : "+ file_name)
    return (file_name, success)

# search files
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
    
#@range_begin(walk)
    for hexpath in dir_walk(args.dir):
        f, s = test(@<b>|os.path.abspath(args.rom),| os.path.abspath(hexpath))
        res_strs.append(("PASS" if s else "FAIL") + " : " + f)
        res_statuses.append(s)
#@range_end(walk)

    res_strs = sorted(res_strs)
    statusText = "Test Result : " + str(sum(res_statuses)) + " / " + str(len(res_statuses))

    with open(os.path.join(args.output_dir, "result.txt"), "w", encoding='utf-8') as f:
        f.write(statusText + "\n")
        f.write("\n".join(res_strs))

    print(statusText)

    if sum(res_statuses) != len(res_statuses):
        exit(1)
