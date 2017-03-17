Core Concepts of Spatial Information - JavaScript
=============================================

Abstract: A JavaScript implementation of the core concepts.
This JavaScript API is designed to provide experts outside GIS domain an easy-to-use spatial computing library over the Web.
It is built on top of ArcGIS JavaScript API 3.x, and uses Dojo toolkit to ensure simplicity and efficiency.

See the [Readme](../README.md) in the parent directory for general information about the Core Concepts.

Contents
----------------------
- [`examples/`](examples): Usage examples of implementations.
- [`test/`](test): Unit tests. (WIP)
- `CcField.js`: Implementations of fields.
- `CcObject.js`: Implementations of objects.

Use the API
-----------------------------------------

#### 1. Configure Dojo with dojoConfig
```
<!-- Configure Dojo first -->
<script>
    dojoConfig = {
        packages: [
            {
                name: "CoreConcepts",
                //the location of the package; can either be a path relative to your server or an absolute path.
                //Suppose the package path is "http://hostname/CoreConceptsJs/"
                location: "/CoreConceptsJs"
            }
        ]
    };
</script>
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

Dependencies
----------------------
- [ArcGIS JavaScript API] (https://developers.arcgis.com/javascript/3/) (Version: 3.x)
- [Dojo] (http://dojotoolkit.org/)

\* Dojo is included with the ArcGIS JavaScript API so there is no need to host/reference/install it.
