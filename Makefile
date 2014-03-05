all: test

install:
	-git clone --depth 1 --branch master --single-branch  https://github.com/hayaku/tests.git test

test: install
	make -f ./test/makefile test

.PHONY: all install test
