VERYL = veryl

build:
	$(VERYL) build
	python3 replace.py
fmt:
	$(VERYL) fmt
check:
	$(VERYL) fmt --check
	$(VERYL) check
clean:
	$(VERYL) clean