#
# Makefile for Core Concepts Python library
# 
# ====== VARIABLES ======

# ====== TARGETS ======
all:
	@echo "Select an option.";
	@cat Makefile;
	@echo "\n";

clean:
	-rm -f *.pyc;

test: clean
	python -m unittest discover;

test-networks: clean
	python -m unittest networks_test;

test-events: clean
	python -m unittest events_test;

test-all: test test-networks test-events
