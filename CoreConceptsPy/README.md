Core Concepts of Spatial Information - Python
=============================================

Abstract: A Python implementation of the core concepts.

The implementation is devided into abstract definitions (`coreconcepts.py`),
implementation of one core concept per file (`events.py`, `fields.py`, `locations.py`, `networks.py` and `objects.py`)
and unit tests (`test/`) and additionally into examples (`examples/`) to showcase the different possibilities of the core concepts.

See the [Readme](../README.md) in the parent directory for more information about the core concepts itself.

Right now the implementation is in a proof of concept state and should not be considered stable for a production environment.

Contents
----------------------

- `coreconcepts.py`: Abstract concepts.
- `events.py`: Implementations of events.
- `examples/`: Usage examples of implementations.
- `fields.py`: Implementations of fields.
- `locations.py`: Implementations of locations.
- `Makefile`: Common commands for unix platforms.
- `makefile.py`: Common commands for non-unix platforms.
- `networks.py`: Implementations of networks.
- `objects.py`: Implementations of objects.
- `test/`: Unit tests.
- `utils.py`: Utilities.
- `RdfReader.py`: Abstract Reader to turn RDF into python objects.
- `RdfWriter.py`: Abstract Writer to turn RDF into python objects.

How to test the code and run the examples
-----------------------------------------

### Unix/Linux platforms
To run the Unit Tests execute: `make test-all`

To run the examples execute: `make example-all`

### Platforms without `make` (like Windows) [WIP]
To run the Unit Tests execute: `python makefile.py test-all`

To run the Examples execute: `python makefile.py example-all`

How to test the code and run the examples
-----------------------------------------

### Unix/Linux platforms
To run the Unit Tests execute: `make test-all`

To run the examples execute: `make example-all`

Dependencies
----------------------
- [GDAL] (http://www.gdal.org) (Version: latest*)
- [NumPy] (http://www.numpy.org) (Version: latest*)
- [NetworkX] (https://networkx.github.io/) (Version: 1.9.1)

\* Most recent stable release

### Unix/Linux platforms
To install the dependencies execute: `make install-dependencies`
