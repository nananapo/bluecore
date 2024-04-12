CORE = core

FILELISTS = $(CORE)/$(CORE).f $(CORE)/sv.f
TOPMODULE = core_top

OPTION = ""
MEMFILE = ""
CYCLE=

build:
	make -C $(CORE)

verilator: build
	verilator $(OPTION) -DFILEPATH=\"$(MEMFILE)\" --cc $(addprefix -f ,$(FILELISTS)) --top-module $(TOPMODULE) --exe src/tb.cpp
	make -C obj_dir/ -f V$(TOPMODULE).mk
	obj_dir/V$(TOPMODULE) $(CYCLE)

iverilog: build
	mkdir -p obj_dir
	iverilog -g2012 $(OPTION) -DFILEPATH=\"$(MEMFILE)\" $(addprefix -f ,$(FILELISTS)) -m $(TOPMODULE) -o obj_dir/a.out
	vvp obj_dir/a.out

fmt:
	make fmt -C $(CORE)

check:
	make check -C $(CORE)

clean:
	make -C $(CORE) clean
	rm -rf obj_dir
