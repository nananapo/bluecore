import sys
import logutil

last_clock = None
stage_ids = dict()
inst_dict = dict()

class Inst:
    def __init__(self):
        self.addr = None
        self.inst = None
        self.last_stage = None

def print_konata(data):
    global last_clock, stage_ids, inst_dict

    # print clock
    clock = data["clock"]
    if last_clock is None:
        last_clock = clock - 1
    print("C",  clock - last_clock, sep="\t")
    last_clock = clock

    new_ids = dict()
    for stage, subs in data.items():
        if stage == "clock":
            continue
        if "inst_id" not in subs:
            continue
        inst_id = subs["inst_id"].get_int_value()

        # register inst_id
        if inst_id not in inst_dict:
            print("I", inst_id, inst_id, 0, sep="\t")
            inst_dict[inst_id] = Inst()
        new_ids[stage] = inst_id

        inst = inst_dict[inst_id]

        # label inst_id
        if inst.addr is None:
            if "addr" in subs:
                addr = str(subs["addr"])
                inst.addr = addr
                print("L", inst_id, 0, addr, sep="\t")
        if inst.addr is not None and inst.inst is None:
            if "inst" in subs:
                bits = str(subs["inst"])
                inst.inst = bits
                print("L", inst_id, 0, ":" + bits, sep="\t")

        # start stage
        if stage not in stage_ids or stage_ids[stage] != inst_id:
            print("S", inst_id, 0, stage, sep="\t")
            inst.last_stage = stage

    # end stage
    for stage, old_inst_id in stage_ids.items():
        if stage in new_ids and new_ids[stage] == old_inst_id:
            continue
        print("E", old_inst_id, 0, stage, sep="\t")
        if stage == "wb":
            del inst_dict[old_inst_id]

    # flush
    if "flush" in data:
        ids = list(inst_dict.keys())
        for inst_id in ids:
            inst = inst_dict[inst_id]
            if inst.last_stage in data["flush"]:
                print("R", inst_id, 0, 1, sep="\t")
                del inst_dict[inst_id]
        
    stage_ids = new_ids

if __name__ == "__main__":
    print("Kanata", "0004", sep="\t")

    args = sys.argv[1:]
    if len(args) == 0:
        logutil.process_log("input", print_konata)
    else:
        logutil.process_log("file", print_konata, filepath=args[0])
