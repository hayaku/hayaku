all: test

update-tests:
	-git clone --depth 1 --branch master --single-branch https://github.com/hayaku/tests.git test
	cd test; git pull -u

test:
	make --keep-going -C test hayaku_path="$(shell pwd)"

.PHONY: all test update-tests
