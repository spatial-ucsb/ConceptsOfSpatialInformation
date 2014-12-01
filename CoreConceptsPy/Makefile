# 
# Makefile for Core Concepts
#
# Andrea Ballatore
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
	python -m unittest discover networks_test;
