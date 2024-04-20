CORE = core

PWD := $(shell pwd)/

FILELISTS := $(CORE)/$(CORE).f
FILELISTS_AB = $(addprefix $(PWD),$(FILELISTS))
TOPMODULE = core_top

OBJDIR = "obj_dir/"

MDIR = ""
OPTION = ""
MEMFILE = ""
CYCLE=

build:
	make -C $(CORE)

fmt:
	make fmt -C $(CORE)

check:
	make check -C $(CORE)

verilator:
	mkdir -p $(OBJDIR)$(MDIR)
	verilator --Mdir $(OBJDIR)$(MDIR) $(OPTION) -DMEMORY_INITIAL_FILE=\"$(MEMFILE)\" --cc $(addprefix -f ,$(FILELISTS_AB)) --top-module $(TOPMODULE) --exe $(PWD)src/tb.cpp
	make -C $(OBJDIR)$(MDIR)/ -f V$(TOPMODULE).mk
	$(OBJDIR)$(MDIR)/V$(TOPMODULE) $(CYCLE)

iverilog:
	mkdir -p $(OBJDIR)$(MDIR)
	iverilog -g2012 $(OPTION) -DMEMORY_INITIAL_FILE=\"$(MEMFILE)\" $(addprefix -f ,$(FILELISTS_AB)) -m $(TOPMODULE) -o $(OBJDIR)$(MDIR)/a.out
	vvp $(OBJDIR)$(MDIR)/a.out

clean:
	make -C $(CORE) clean
	rm -rf obj_dir

.PHONY: build verilator iverilog fmt check clean