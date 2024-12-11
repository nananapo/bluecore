class LogData:
    def __init__(self, print_type, str_value):
        self.print_type = print_type
        self.str_value = str_value
    def get_int_value(self):
        if self.print_type not in "bdh":
            return None
        return int(self.str_value, 2)
    def __str__(self):
        if self.print_type == "b":
            return self.str_value
        if self.print_type == "d":
            return str(int(self.str_value, 2))
        if self.print_type == "h":
            s = hex(int(self.str_value, 2))[2:]
            zc = (len(self.str_value) + 3) // 4 - len(s)
            return "0" * zc + s
        return self.str_value

def parse(readline, is_file=False):
    data = dict()
    read_clock = False

    try:
        while True:
            l = readline()

            if is_file and not l:
                break

            l = l.rstrip("\r\n")
            sp = l.split(",")
            if len(sp) <= 1:
                continue
            
            id = sp[0]
            if len(sp) == 2 and id == "clock":
                if read_clock:
                    yield data
                read_clock = True
                data = dict()
                data["clock"] = int(sp[1])
                continue
            
            if len(sp) > 2:
                print_type = sp[1]
                value = ",".join(sp[2:])
            
                idsp = id.split(".")
                id_root = idsp[0]
                id_sub = None
                if len(idsp) > 1:
                    id_sub = ".".join(idsp[1:])

                if id_root not in data:
                    data[id_root] = dict()
                data[id_root][id_sub] = LogData(print_type, value)
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
    yield data

def process_log(mode, func, filepath = None):
    if mode == "input":
        for data in parse(input):
            if data is None:
                break
            func(data)
    elif mode == "file":
        with open(filepath, mode="r") as fd:
            for data in parse(fd.readline, is_file=True):
                if data is None:
                    break
                func(data)
    else:
        raise ValueError("unknown mode : " + str(mode))
