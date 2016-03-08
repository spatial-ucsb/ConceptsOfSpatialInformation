Core Concepts of Spatial Information - Haskell
==============================================

Abstract: Specifications and implementation of the core concepts in Haskell.

See the [Readme](../README.md) in the parent directory for more information about the core concepts itself.

Right now the implementation is in a proof of concept state and should not be considered stable for a production environment.

Contents
----------------------

- `Event.hs`: Specifications of events.
- `Field.hs`: Specifications of fields.
- `Location.hs`: Specifications of locations.
- `Makefile`: Common commands for unix platforms.
- `NetworkExamples.hs`: Examples for networks.
- `Network.hs`: Specifications of networks.
- `NetworkImpl.hs`: Implementations of networks.
- `Object.hs`: Specifications of objects.

How to test the code and run the examples
-----------------------------------------

### Unix/Linux platforms
To run the Unit Tests execute: `make test-all`

To run the examples execute: `make example-all`

Dependencies
----------------------
- [FGL](https://hackage.haskell.org/package/fgl) (Version: latest*)

\* Most recent stable release on hackage

### Unix/Linux platforms
To install the dependencies execute: `make install-dependencies`
