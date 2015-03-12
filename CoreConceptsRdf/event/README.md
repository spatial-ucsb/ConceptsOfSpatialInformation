Core Concepts of Spatial Information - RDF event ontologies
===========================================================

Abstract: RDF schema and ontologies of the event core concept.

Contents
----------------------

* `examples/`: RDF event examples.
* `coreconcepts_rdfs.rdf`: RDF Schema of the Core Concepts.
* `event_rdfs.rdf`: RDF Schema of the Event Core Concept.
* `event_ttl.owl`: OWL ontology of the Event Core Concept written in Turtle syntax.
* `event_xml.owl`: OWL ontology of the Event Core Concept written in RDF/XML syntax.
* `event_xml_2.owl`: OWL ontology of the Event Core Concept that makes use of the owl time ontology.


Use Guide
----------------------
1. Install [Virtuoso](http://virtuoso.openlinksw.com/)

2. Choose an ontology

    You can choose (`event_rdfs.rdf`), (`event_xml.owl`) or (`event_xml_2.owl`).

3. Use Virtuoso to upload the ontology into a graph
    - Start a Virtuoso Instance
    - Open the Virtuoso Conductor and login
    - Open the tab "Linked Data"
    - Open the subtab "Quad Store Upload"
    - Upload the ontology file and name your graph

4. Setup a rule for the ontology

    To use an ontology with SPARQL queries you need to setup a rule for the ontology.

    - In the Virtuoso Conductor open the tab "Database"
    - Open the subtab "Interactive SQL"
    - Use the SQL command `rdfs_rule_set("rule-name", "graph-uri")` to set the uploaded ontology as a new rule. Specify a name for the rule and use the graph uri of the previously uploaded ontology.

    Example:
    `rdfs_rule_set ('owl-rules-1', 'http://localhost:8890/owl-ontology');`

    In this example the rule name is 'owl-rules-1' and the graph uri of the ontology is 'http://localhost:8890/owl-ontology'.

    All rules are stored in the table `DB.DBA.SYS_RDF_SCHEMA`. You can query the table to check, if your new rule was successfully added: `SELECT * FROM DB.DBA.SYS_RDF_SCHEMA`

5. Upload RDF data

    Upload RDF data that uses this ontology into another graph. You can use your own data or choose from existing RDF files. Depending on your ontology selection in step 2 you can use the following files:

    - For (`event_rdfs.rdf`) use (`examples/ontology/rdfs_ontology.rdf`)
    - For (`event_xml.owl`) use (`examples/ontology/owl_ontology.rdf`).
    - For (`event_xml_2.owl`) use (`examples/ontology/owl_ontology_2.rdf`)

6. Query the data

    Query the uploaded RDF graph while using the ontology as a rule.

    - In the Virtuoso Conductor open the tab "Database"
    - Open the subtab "Interactive SQL"
    - To use an ontology in a SPARQL query you need to supply the rule of that ontology. Set the rule of the SPARQL query with the rule name you defined in step 4: `SPARQL DEFINE input:inference "your-rule-name"`
    - Specify the uri of the RDF data graph after the FROM statement in angle brackets.
    - Write your query

    Example:

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

    This example uses the rule named "owl-rules-1" and queries the RDF graph with the uri "http://localhost:8890/event-data".
