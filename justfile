alias t := testall
alias test := testall

[no-exit-message]
testall:
	#! /usr/bin/env sh
	echo "=== Running tests in all packages ==="
	for d in packages/*; do
	if [ -f $d/justfile ]; then
	echo "=== Running tests in $d ==="
	just $d/test
	fi
	done
