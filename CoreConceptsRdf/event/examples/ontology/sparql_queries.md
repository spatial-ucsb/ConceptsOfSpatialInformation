SPARQL Queries
=============================================

This file contains SPARQL queries to test the event owl ontology (`event_xml.owl`) located in the (`CoreConceptsRdf`) folder.
The file (`owl-ontology.rdf`) contains RDF event examples using this owl ontology.

The owl ontology was loaded in a graph named "http://localhost:8890/owl-ontology" on a local Virtuoso server.
The Virtuoso SQL interface was used to set the ontology as a new rule so that inference could be used.
The SQL command "rdfs_rule_set ('owl-rules-1', 'http://localhost:8890/owl-ontology');" was used to setup the rule named "owl-rules-1" with the ontology graph.
The event example RDF was loaded in a separate graph named "http://localhost:8890/event-data".

To test the inference capabilites of the owl ontology the following Sparql queries were run against the graph:

**Transitive test for the before property 

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:before evs:basketball
  }
```

Result
* http://www.core-concepts.com/events/baseball
* http://www.core-concepts.com/events/soccer


**Transitive test for the after property 

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:after evs:hockey
  }
```

Result
* http://www.core-concepts.com/events/climbing
* http://www.core-concepts.com/events/tennis


**Transitive test for the during property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:during evs:golf
  }
```

Result
* http://www.core-concepts.com/events/football
* http://www.core-concepts.com/events/ultimate-frisbee


**Symmetric test for the temporalOverlap property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:temporalOverlap evs:snowboarding-tournament
  }
```

Result
* http://www.core-concepts.com/events/ski-tournament


**Symmetric test for the temporalIntersection property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:temporalIntersection evs:checkers-match
  }
```

Result
* http://www.core-concepts.com/events/chess-match


**Inverse test for before/after property

```
SPARQL DEFINE input:inference "owl-rules-1"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>

SELECT *
FROM <http://localhost:8890/event-data>
WHERE
  {
    ?s rdf:type ev:Event;
          ev:after evs:baseball
  }
```

Result
* http://www.core-concepts.com/events/basketball
* http://www.core-concepts.com/events/soccer