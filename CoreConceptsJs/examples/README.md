Core Concepts of Spatial Information - JavaScript usage examples
=============================================

Abstract: Usage examples for JavaScript implementation of the core concepts.

Contents
----------------------

- `nightlight.html`: a nighttime lights case study which can be viewed as a field-based question. This question is raised
 by Mat Lowe who use night lights as a proxy to measure the level of economic activities (Lowe 2014). Instead of procedural
 steps that Lowe uses to answer his spatial question, this example shows how we address it using core concepts solution.

Core concepts solutions
-----------------------------------------

### Example 1: Night lights
Lowe's question can be summarised as "What was the night time luminosity for the year 1994, near roads in mainland China,
excluding gas flares, on a 0.1 degree grid?" The problem-solving process involves translating spatial questions into the
core concepts of spatial information and operations applied to them.
- Conceptualize luminosity as a **`field`**
- state the field `**domain**`: *inside* 0.5 degrees from China roads, *outside* gas flares
- state the field **granularity**: 0.1 degree

Data involved in this example: (1)two global nocturnal luminosity maps (url_lights_F10, and url_lights_F12); (2) a map of roads
in mainland China(url_china_roads); (3)a map of gas flares (url_china_flares).

#### (1) load input data
```

```
\* Keep in mind you must set the dojoConfig variable before loading ArcGIS JS API
#### 2. Reference the ArcGIS API for JavaScript
Use a second \<script\> to load the ArcGIS API for JavaScript from CDN
```
<script src="https://js.arcgis.com/3.19/"></script>
```
#### 3. Load modules
Use `require` to load specific modules from the API. The first parameter to `require` is an array of module ids
— identifiers for the modules you want to load, and the second parameter is a callback function.
```
<script>
  require(["CoreConcepts/CcField"], function(CcField) { ... });
</script>
```
\* You can also get started by taking a look at test files or examples.

References
----------
- Lowe, M. (2014). *Night lights and ArcGis: A brief guide.* Avaliable online: http://economics. mit. edu/files/8945 (accessed on 3 March 2017).
- Vahedi, B., Kuhn, W., Ballatore A. (2016). *Question-Based Spatial Computing - A Case Study.* In T. Sarjakoski, M. Y. Santos, & L. T. Sarjakoski (Eds.), Lecture Notes in Geoinformation and Cartography (AGILE 2016) (pp. 37 - 50). Berlin: Springer. <[PDF](https://link.springer.com/chapter/10.1007/978-3-319-33783-8_3)>
