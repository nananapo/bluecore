VERYL = ../../veryl/target/debug/veryl

build:
	$(VERYL) build
	python3 comp.py
fmt:
	$(VERYL) fmt
check:
	$(VERYL) fmt --check
	$(VERYL) check
clean:
	$(VERYL) clean