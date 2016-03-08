#
# Makefile for Core Concepts Haskell library
#
# ====== VARIABLES ======

# ====== TARGETS ======
all:
	@echo "Select an option.";
	@cat Makefile;
	@echo "\n";

clean:
	@rm -rf *.hi **/*.hi *.o **/*.o;

test-events: clean
	@echo "No examples and no tests for events yet."

test-fields: clean
	@echo "No examples and no tests for fields yet."

test-locations: clean
	@echo "No examples and no tests for locations yet."

test-networks: clean
	@echo "No tests for networks yet. Have a look at the examples."

test-objects: clean
	@echo "No examples and no tests for objects yet."

test-all: test-events test-fields test-locations test-networks test-objects

example-events: clean
	@echo "No examples and no tests for events yet."

example-fields: clean
	@echo "No examples and no tests for fields yet."

example-locations: clean
	@echo "No examples and no tests for locations yet."

example-networks: clean
	runhaskell NetworkExamples.hs

example-objects: clean
	@echo "No examples for objects yet. Have a look at the tests."

example-all: example-events example-fields example-locations example-networks example-objects

install-dependencies:
	# for Linux/Mac
	cabal install fgl;
