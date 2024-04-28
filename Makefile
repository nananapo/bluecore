CORE = core

PWD := $(shell pwd)/

FILELISTS := $(CORE)/$(CORE).f
FILELISTS_AB = $(addprefix $(PWD),$(FILELISTS))
TOPMODULE = core_top

OBJDIR = obj_dir/

MDIR = ""
OPTION = ""
MEMFILE = ""

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
	echo executable file: $(OBJDIR)$(MDIR)/V$(TOPMODULE)

clean:
	make -C $(CORE) clean
	rm -rf obj_dir results

.PHONY: build verilator iverilog fmt check clean
