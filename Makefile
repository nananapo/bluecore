CORE = core

PWD := $(shell pwd)/

FILELISTS := $(CORE)/$(CORE).f $(CORE)/sv.f
FILELISTS_AB = $(addprefix $(PWD),$(FILELISTS))
TOPMODULE = core_top

MDIR = "obj_dir/"
OPTION = ""
MEMFILE = ""
CYCLE=

build:
	make -C $(CORE)

verilator:
	mkdir -p $(MDIR)
	verilator --Mdir $(MDIR) $(OPTION) -DFILEPATH=\"$(MEMFILE)\" --cc $(addprefix -f ,$(FILELISTS_AB)) --top-module $(TOPMODULE) --exe $(PWD)src/tb.cpp
	make -C $(MDIR)/ -f V$(TOPMODULE).mk
	$(MDIR)/V$(TOPMODULE) $(CYCLE)

iverilog:
	mkdir -p $(MDIR)
	iverilog -g2012 $(OPTION) -DFILEPATH=\"$(MEMFILE)\" $(addprefix -f ,$(FILELISTS_AB)) -m $(TOPMODULE) -o $(MDIR)/a.out
	vvp $(MDIR)/a.out

fmt:
	make fmt -C $(CORE)

check:
	make check -C $(CORE)

clean:
	make -C $(CORE) clean
	rm -rf obj_dir
