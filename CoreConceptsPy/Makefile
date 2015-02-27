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
	@rm -f *.pyc;
	@rm -f test/*.pyc;
	@rm -f examples/*.pyc;
	@rm -f examples/events/*.pyc;
	@rm -f examples/fields/*.pyc;
	@rm -f examples/locations/*.pyc;
	@rm -f examples/networks/*.pyc;
	@rm -f examples/objects/*.pyc;

test-events: clean
	python -m unittest discover -s 'test' -p 'events_test.py' -t '..';

test-fields: clean
	python -m unittest discover -s 'test' -p 'fields_test.py' -t '..';

test-locations: clean
	@echo "No examples and no tests for locations yet."

test-networks: clean
	python -m unittest discover -s 'test' -p 'networks_test.py' -t '..';

test-objects: clean
	python -m unittest discover -s 'test' -p 'objects_test.py' -t '..';

test-all: clean
	python -m unittest discover -s 'test' -p '*_test.py' -t '..';

example-events: clean
	python examples/events/example-1.py
	python examples/events/example-2.py
	python examples/events/example-3.py

example-fields: clean
	@echo "No examples for fields yet. Have a look at the tests."

example-locations: clean
	@echo "No examples and no tests for locations yet."

example-networks: clean
	python examples/networks/karate.py
	python examples/networks/fake_weighted_network.py
	python examples/networks/ucsb.py

example-objects: clean
	@echo "No examples for objects yet. Have a look at the tests."

example-all: example-events example-fields example-locations example-networks example-objects

install_py_dependencies:
	# for Linux/Mac
	easy_install networkx;
	# TODO: install other dependencies
