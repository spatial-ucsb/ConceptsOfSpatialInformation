<!---
Abstract: Sparql queries to test the event owl ontology "event_xml.owl" located in the "CoreConceptsRdf" folder with real event RDF data from
"owl_ontology_3.rdf".
Author: Marc Tim Thiemann
-->

SPARQL Queries
=============================================

This file contains SPARQL queries to test the event owl ontology (`event_xml.owl`) located in the (`CoreConceptsRdf`) folder.
The file (`owl-ontology_3.rdf`) contains RDF event examples with real event data using this owl ontology.

The owl ontology was loaded in a graph named "http://localhost:8890/owl-ontology" on a local Virtuoso server.
The Virtuoso SQL interface was used to set the ontology as a new rule so that inference could be used.
The SQL command "rdfs_rule_set ('owl-rules-1', 'http://localhost:8890/owl-ontology');" was used to setup the rule named "owl-rules-1" with the ontology graph.
The event example RDF was loaded in a separate graph named "http://localhost:8890/event-data".

To test the inference capabilites of the owl ontology the following Sparql queries were run against the graph:

**Transitive test for the before property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX eqs: <http://www.core-concepts.com/events/earthquake/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
    ?event rdf:type ev:Event;
          ev:before eqs:4978f1066e8cddf51e72555962138292
  }
```

Result
* http://www.core-concepts.com/events/earthquake/25659f600c9afff060d4a5427fa1fa95
* http://www.core-concepts.com/events/earthquake/4978f1066e8cddf51e72555962138292


**Transitive test for the after property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX eqs: <http://www.core-concepts.com/events/earthquake/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
    ?event rdf:type ev:Event;
          ev:after eqs:cc16e1b39c2fa1dc9b79369570ab12e7
  }
```

Result
* http://www.core-concepts.com/events/earthquake/1ec8007ed339685f251ec75f1c0c6ac7
* http://www.core-concepts.com/events/earthquake/b6915b5c2e13a466ebf45dac9eaf4ce5


**Transitive test for the during property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX weather: <http://www.core-concepts.com/events/weather/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
    ?event rdf:type ev:Event;
          ev:during weather:b9d5e185e3a89aa5dfa47766dedc12a8
  }
```

Result
* http://www.core-concepts.com/events/weather/7ea9bb7b37dbe63074e61de46f3a82dd
* http://www.core-concepts.com/events/weather/befa1fd6d5237a7880786ba16f935225


**Symmetric test for the temporalOverlap property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX cl: <http://www.core-concepts.com/events/class/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
     cl:2f51a3827f3a558449c51d6a9d1e7d74 ev:temporalOverlap ?overlapsWith
  }
```

Result
* http://www.core-concepts.com/events/class/b4cc6c8d4e4c6c7d11d715d4c8f8022e


**Symmetric test for the temporalIntersection property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX cl: <http://www.core-concepts.com/events/class/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
     cl:712fc5d39fdb5ed768635035b5d19a11 ev:temporalIntersection ?intersectsWith
  }
```

Result
* http://www.core-concepts.com/events/class/de03b9f182888b848ba1c2f061e69f63


**Inverse test for before/after property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX eqs: <http://www.core-concepts.com/events/earthquake/>

SELECT *
FROM <http://localhost:8890/event-data-3>
WHERE
  {
     eqs:4978f1066e8cddf51e72555962138292 ev:after ?events
  }
```

Result
* http://www.core-concepts.com/events/earthquake/25659f600c9afff060d4a5427fa1fa95
* http://www.core-concepts.com/events/earthquake/01331aa855fa28da5b5ccd40b6213d32
