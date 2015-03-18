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
	@rm -rf *.pyc **/*.pyc tmp;
	@mkdir tmp;

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
	python examples/events/example_1.py
	python examples/events/example_2.py
	python examples/events/example_3.py
	python examples/events/earthquake/output_use_case.py
	python examples/events/earthquake/input_use_case.py

example-fields: clean
	@echo "No examples for fields yet. Have a look at the tests."

example-locations: clean
	@echo "No examples and no tests for locations yet."

example-networks: clean
	python examples/networks/karate.py
	python examples/networks/synthetic_weighted_network.py
	python examples/networks/ucsb.py

example-objects: clean
	@echo "No examples for objects yet. Have a look at the tests."

example-all: example-events example-fields example-locations example-networks example-objects

install-dependencies:
	# for Linux/Mac
	sudo pip install networkx;
	@echo "Make sure, that you have installed GDAL and NumPy!"
