<!---
Abstract: Sparql queries for the earthquake class RDF output located in the file "test.rdf".
Author: Marc Tim Thiemann
-->

SPARQL Queries
=============================================

This file contains example SPARQL queries for the earthquake class RDF output located in the file `test.rdf`.
The RDF file was loaded in a graph on a local Virtuoso server and the following SPARQL queries were run against the RDF graph.

Get all earthquakes with a magnitude of 2.5 or higher:

```
PREFIX eq: <http://myearthquakes.com/>
PREFIX lode: <http://linkedevents.org/ontology/>

SELECT ?latitude ?longitude ?place ?time ?magnitude WHERE {
    ?s rdf:type eq:Earthquake;
    dbpprop:magnitude ?magnitude;
    geo:lat ?latitude;
    geo:long ?longitude;
    lode:atTime ?time;
    lode:atPlace ?place
FILTER(?magnitude > 2.5)
}
ORDER BY ?magnitude
```


Get all earthquakes of the first 7 days of December 2014:

```
PREFIX eq: <http://myearthquakes.com/>
PREFIX lode: <http://linkedevents.org/ontology/>

SELECT ?latitude ?longitude ?place ?time ?magnitude WHERE {
    ?s rdf:type eq:Earthquake;
    dbpprop:magnitude ?magnitude;
    geo:lat ?latitude;
    geo:long ?longitude;
    lode:atTime ?time;
    lode:atPlace ?place
FILTER (?time < "2014-12-06T23:59:59-08:00"^^xsd:dateTime)
}
ORDER BY ?time
```


Get all earthquakes in the Northern hemisphere:

```
PREFIX eq: <http://myearthquakes.com/>
PREFIX lode: <http://linkedevents.org/ontology/>

SELECT ?latitude ?longitude ?place ?time ?magnitude WHERE {
    ?s rdf:type eq:Earthquake;
    dbpprop:magnitude ?magnitude;
    geo:lat ?latitude;
    geo:long ?longitude;
    lode:atTime ?time;
    lode:atPlace ?place
FILTER (?latitude >= 0)
}
ORDER BY ?latitude
```


Get all earthquakes in the Western Hemisphere:

```
PREFIX eq: <http://myearthquakes.com/>
PREFIX lode: <http://linkedevents.org/ontology/>

SELECT ?latitude ?longitude ?place ?time ?magnitude WHERE {
    ?s rdf:type eq:Earthquake;
    dbpprop:magnitude ?magnitude;
    geo:lat ?latitude;
    geo:long ?longitude;
    lode:atTime ?time;
    lode:atPlace ?place
FILTER(?longitude < 0)
}
ORDER BY DESC(?longitude)
```


Get all earthquakes near California:

```
PREFIX eq: <http://myearthquakes.com/>
PREFIX lode: <http://linkedevents.org/ontology/>

SELECT ?latitude ?longitude ?place ?time ?magnitude WHERE {
    ?s rdf:type eq:Earthquake;
    dbpprop:magnitude ?magnitude;
    geo:lat ?latitude;
    geo:long ?longitude;
    lode:atTime ?time;
    lode:atPlace ?place
FILTER regex(?place, "California", "i")
}
ORDER BY ?magnitude
```
