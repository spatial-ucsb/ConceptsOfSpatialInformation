RDF input and output with earthquake data
==================================================

Abstract: Create RDF input and output with earthquake data using RDF readers and writers and an earthquake model.

The Earthquake class (`earthquake.py`) works as a model for each earthquake.

There are two RdfReaders that turn RDF input into earthquake python objects:
(`EarthquakeRdfReader.py`) inherits from (`RdfReader.py`) which is an abstract implementation of a RdfReader.
(`EarthquakeRdfReader2.py`) does not inherit from that abstract RdfReader.

Similarly, there are two RdfWriters that turn Earthquake python objects into RDF:
(`EarthquakeRdfWriter.py`) inherits from (`RdfWriter.py`) which is an abstract implementation of a RdfWriter.
(`EarthquakeRdfWriter2.py`) does not inherit from that abstract RdfWriter.

Both RdfReaders and RdfWriters are used in the (`input_use_case.py`) and (`output_use_case.py`) file, respectively.

The (`bindings.json`) file works as a configuration file for RDF prefix/namespace bindings for RdfReaders and RdfWriters.

RDF input and output files used for this example can be found in the folder (`CoreConceptsRdf/examples/events/earthquake/`).

Contents
----------------------

* `earthquake.py`: Earthquake class.
* `EarthquakeRdfReader.py`: Reads Earthquake RDF and turns it into Earthquake python objects (inherits from RdfReader).
* `EarthquakeRdfReader2.py`: Reads Earthquake RDF and turns it into Earthquake python objects (does not inherit from RdfReader).
* `EarthquakeRdfWriter.py`: Writes Earthquake python objects to RDF (inherits from RdfWriter).
* `EarthquakeRdfWriter2.py`: Writes Earthquake python objects to RDF (does not inherit from RdfWriter).
* `input_use_case.py`: Use case with RDF input and python output.
* `output_use_case.py`: Use case with python input and RDF output.
* `bindings.json`: json configuration file for RDF prefix/namespace bindings.

Dependencies
----------------------

* rdflib (4.2.1) <http://www.rdflib.net>
