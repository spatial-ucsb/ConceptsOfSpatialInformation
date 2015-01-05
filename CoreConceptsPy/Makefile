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
	rm -f *.pyc;
	rm -f test/*.pyc;
	rm -f examples/*.pyc;
	rm -f examples/events/*.pyc;
	rm -f examples/fields/*.pyc;
	rm -f examples/locations/*.pyc;
	rm -f examples/networks/*.pyc;
	rm -f examples/objects/*.pyc;

test-events: clean
	python -m unittest discover -s 'test' -p 'events_test.py' -t '..';

test-fields: clean
	python -m unittest discover -s 'test' -p 'fields_test.py' -t '..';

test-networks: clean
	python -m unittest discover -s 'test' -p 'networks_test.py' -t '..';

test-objects: clean
	python -m unittest discover -s 'test' -p 'objects_test.py' -t '..';

test-all: clean
	python -m unittest discover -s 'test' -p '*_test.py' -t '..';

install_py_dependencies:
	# for Linux/Mac
	easy_install networkx;
	# TODO: install other dependencies
