import sys
import logutil

def print_readable_log(data):
    clock = data["clock"]
    print("#", clock)

    for id, subs in data.items():
        if id == "clock":
            continue
        if len(subs) == 1 and None in subs:
            print(id, ":", subs[None])
            continue

        print(id, "------------")
        key_max_len = max(map(lambda x:len(str(x)), subs.keys()))
        values = []
        for sid, value in subs.items():
            sid = str(sid)
            spaces = " " * (key_max_len - len(sid))
            print(" ", sid + spaces, ":", str(value))
            

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        logutil.process_log("input", print_readable_log)
    else:
        logutil.process_log("file", print_readable_log, filepath=args[0])
