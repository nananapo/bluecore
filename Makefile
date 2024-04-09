CORE = core

FILELISTS = $(CORE)/$(CORE).f $(CORE)/sv.f
TOPMODULE = core_top

OPTION = ""
MEMFILE = ""

build:
	make -C $(CORE)

run: # clean build
	verilator $(OPTION) -DFILEPATH=\"$(MEMFILE)\" --cc $(addprefix -f ,$(FILELISTS))  --top-module $(TOPMODULE) --exe src/tb.cpp
	make -C obj_dir/ -f V$(TOPMODULE).mk
	obj_dir/V$(TOPMODULE)

fmt:
	make fmt -C $(CORE)

clean:
	make -C $(CORE) clean
	rm -rf obj_dir