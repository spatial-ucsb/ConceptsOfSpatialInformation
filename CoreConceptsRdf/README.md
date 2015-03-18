Core Concepts of Spatial Information - RDF
=============================================

Abstract: RDF files and ontologies

Contents
----------------------

* `event/`: RDF event ontologies and examples.
* `coreconceps_rdfs.rdf`: Preliminary RDF schema of the core concepts


RDFS vs. OWL
----------------------
OWL offers extended functionality on top of RDFS. OWL ontologies still need to use RDFS terms such as `rdfs:range`, `rdfs:domain`, `rdfs:subClassOf`, `rdfs:subPropertyOf`, `rdfs:label`, `rdfs:comment` because OWL does not offer this functionality.

Additional functionalities of OWL are:

####Property Restrictions

- **value constraints**

    You can define that all values or some values need to come from another class or that a property has a specifc value.

- **cardinality constraints**

    You can define the minimum cardinality, maximum cardinality or the cardinality of a property.

- **FunctionalProperty**

    Assigns a maximum cardinality of 1 to a property.

- **InverseFunctionalProperty**

    Assigns a maximum cardinality of 1 to the inverse property.

####Inference with additional properties

Additional properties make inference possible. You can define the inverse property of a property, the equivalent property of a property and you can make a property transitive or symmetric.

####Versatile class descriptions

You can describe a class as an enumeration, intersection, union and/or complement of other classes. Additionally, you can describe classes with property restrictions.

####Individuals

You can say that an individual is the same as another individual or different from another individual.

####Annotations and Header

You can define a header that contains information about the ontology including version, title, imports of other ontologies, a prior ontology version, the compatibility with that prior version and deprecated classes and properties.
