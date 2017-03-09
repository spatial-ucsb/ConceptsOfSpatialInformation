Core Concepts of Spatial Information - JavaScript usage examples
=============================================

Abstract: Usage examples for JavaScript implementation of the core concepts.

Contents
----------------------

- `nightlight.html`: a nighttime lights case study which can be viewed as a field-based question. This question is raised
 by Matt Lowe who use night lights as a proxy to measure the level of economic activities (Lowe 2014). Instead of procedural
 steps that Lowe uses to answer his spatial question, this example shows how we address it using core concepts solution.

Core concepts solutions
-----------------------------------------

### Example 1: Night lights (TODO)
#### Problem statement:
Lowe's question can be summarised as "What was the night time luminosity for the year 1994, in Mainland China,
excluding gas flares, within 0.5 degrees from roads, on a 0.1 degree grid?"
- Conceptualize luminosity as a **`field`**
- restrict the field **`domain`**: *inside* Mainland China, *inside* 0.5 degrees buffer around roads, *outside* gas flares
- state the field **`granularity`**: 0.1 degree

#### Spatial data involved in this example:
- two global night lights maps (url_lights_F10, and url_lights_F12);
- a boundary map of Mainland China (url_china)
- a map of roads in mainland China (url_china_roads);
- a map of gas flares (url_china_flares).

#### Problem solving:
The problem-solving process involves translating spatial questions into the
core concepts of spatial information and operations applied to them.
#### - Solution A：

#####(1) Interpret luminosity data as fields; boundary, roads and gas flares as objects
```
lights_F10 = new CcField(url_lights_F10);
lights_F12 = new CcField(url_lights_F12);
boundary = new CcObject(url_china);
roads = new CcObject(url_china_roads);
gas_flares = new CcObject(url_china_flares);
```
#####(2) What is the mean luminosity for the year 1994?
```
average_luminosity = lights_F10.local(lights_F12, "average");
```

#####(3) What is the mean luminosity for the year 1994, in Mainland China, excluding gas flares, within 0.5 degrees from roads?
```
//in Mainland China
boundary.getGeometry().then(function(boundary_geometry){
       average_luminosity.restrictDomain(boundary_geometry,"inside");
   });
//excluding gas flares
gas_flares.getGeometry().then(function(flares_geometry){
       average_luminosity.restrictDomain(flares_geometry,"outside");
   });
//within 0.5 degrees from roads
roads.buffer(0.5, "degree").then(function(buffered_geometry){
       average_luminosity.restrictDomain(buffered_geometry,"inside");
   });
```
#####(4) What is the mean luminosity in a 0.1 by 0.1 degree area?
```
average_luminosity.coarsen(0.1, 0.1);
```
#### - Solution B: (WIP)

We could even take it a step further and treat Lowe's question as creating a **field** with a specific **domain**
at a specific **granularity**.
```
//Specifies domain
domain = {"inside": [], "outside": []};
boundary = new CcObject(url_china);
roads = new CcObject(url_china_roads);
gas_flares = new CcObject(url_china_flares);
boundary.getGeometry().then(function(boundary_geometry){
        domain.inside.push(boundary_geometry);
gas_flares.getGeometry().then(function(flares_geometry){
        domain.outside.push(flares_geometry);
   });
roads.buffer(0.5, "degree").then(function(buffered_geometry){
        domain.inside.push(buffered_geometry);
   });

//Specifies granularity
var granularity = [0.1, 0.1];

//Constructs a field with domain and granularity information
lights_F10 = new CcField(url_lights_F10, domain, granularity);
lights_F12 = new CcField(url_lights_F12, domain, granularity);

//Averages two field
average_luminosity = lights_F10.local(lights_F12, "average");
```
References
----------
- Lowe, M. (2014). *Night lights and ArcGIS: A brief guide.* Avaliable online: http://economics.mit.edu/files/8945 (accessed on 3 March 2017).
