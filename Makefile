all: install test

install:
	if [ ! -d "test" ]; then git clone https://github.com/hayaku/tests.git test ; fi

test: install
	make -f ./test/makefile.travis test

.PHONY: all install test
