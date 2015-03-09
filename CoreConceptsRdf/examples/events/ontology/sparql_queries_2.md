SPARQL Queries
=============================================

This file contains SPARQL queries to test how the owl ontology (`CoreConceptsRdf/event_xml_2.owl`) works together with the [owl time ontology] (http://www.w3.org/2006/time#).
The file (`owl-ontology_2.rdf`) contains RDF event examples using this owl ontology.

The owl time ontology was loaded in a graph named "http://localhost:8890/owl-time" on a local Virtuoso server.
The Virtuoso SQL interface was used to set the ontology as a new rule so that inference could be used.
The SQL command "rdfs_rule_set ('owl-time', 'http://localhost:8890/owl-time');" was used to setup the rule named "owl-time" with the ontology graph.
The event example RDF was loaded in a separate graph named "http://localhost:8890/event-data-2".

To test the owl ontology and its inference capabilites the following Sparql queries were run against the graph:

**Transitive test for the before property

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?event
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    ?event rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:before interval:basketball
  }
```

Result
* http://www.core-concepts.com/events/baseball
* http://www.core-concepts.com/events/soccer


**Transitive test for the after property

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?event
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    ?event rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:after interval:hockey
  }
```

Result
* http://www.core-concepts.com/events/climbing
* http://www.core-concepts.com/events/tennis


**Get start time and end time of the golf tournament

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?startTime ?endTime
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    evs:golfTournament rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:hasBeginning ?beginning;
           time:hasEnd ?end .
    ?beginning time:inXSDDateTime ?startTime .
    ?end time:inXSDDateTime ?endTime
  }
```

Result
* startTime: 2015-03-15T10:00:00-8:00
* endTime: 2015-03-15T10:00:00-8:00


**Get start time of the tennis tournament

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?hour ?minute ?day ?dayOfWeek ?dayOfYear ?week ?month ?year ?timeZone
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    evs:tennisTournament rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:hasBeginning ?beginning .
    ?beginning time:inDateTime ?startDateTime .
    ?startDateTime time:hour ?hour;
           time:minute ?minute;
           time:day ?day;
           time:dayOfWeek ?dayOfWeek;
           time:dayOfYear ?dayOfYear;
           time:week ?week;
           time:month ?month;
           time:year ?year;
           time:timeZone ?timeZone
  }
```

Result
* hour: 9
* minute: 0
* day: 14
* dayOfWeek: Saturday
* dayOfYear: 73
* week: 11
* month: 3
* year: 2015
* timeZone: http://www.w3.org/2006/timezone-us#PST


**Get end time of the tennis tournament

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?hour ?minute ?day ?dayOfWeek ?dayOfYear ?week ?month ?year ?timeZone
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    evs:tennisTournament rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:hasEnd ?end .
    ?end time:inDateTime ?endDateTime .
    ?endDateTime time:hour ?hour;
           time:minute ?minute;
           time:day ?day;
           time:dayOfWeek ?dayOfWeek;
           time:dayOfYear ?dayOfYear;
           time:week ?week;
           time:month ?month;
           time:year ?year;
           time:timeZone ?timeZone
  }
```

Result
* hour: 15
* minute: 0
* day: 14
* dayOfWeek: Saturday
* dayOfYear: 73
* week: 11
* month: 3
* year: 2015
* timeZone: http://www.w3.org/2006/timezone-us#PST


**Get start time and duration of football game

```
SPARQL DEFINE input:inference "owl-time"
PREFIX ev: <http://www.core-concepts.com/event#>
PREFIX evs: <http://www.core-concepts.com/events/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX interval: <http://www.core-concepts.com/intervals/>

SELECT ?startTime ?hours ?minutes
FROM <http://localhost:8890/event-data-2>
WHERE
  {
    evs:footballGame rdf:type ev:Event;
          ev:hasTemporalEntity ?entity .
    ?entity time:hasBeginning ?beginning;
          time:hasDurationDescription ?durationDescription .
    ?beginning time:inXSDDateTime ?startTime .
    ?durationDescription time:hours ?hours;
           time:minutes ?minutes .
  }
```

Result
* startTime: 2015-03-13T15:00:00-8:00
* hours: 1
* minutes: 45
