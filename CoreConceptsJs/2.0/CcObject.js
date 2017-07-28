/**
 * JavaScript implementation of the core concept 'object'.
 * The implementation has migrated from ArcGIS JavaScript API 3.x to 4.x
 * version: 2.0.0
 * (c) Liangcun Jiang
 * latest change: July 27, 2017.
 * Dev Notes: Use GeometryEngine instead of GeometryService
 */
define(["dojo/_base/declare",
    "esri/layers/FeatureLayer",
    "esri/tasks/support/Query",
    "esri/tasks/QueryTask",
    "esri/geometry/Multipoint",
    "esri/tasks/GeometryService",
    "esri/geometry/geometryEngine",
    "esri/tasks/support/BufferParameters"
], function (declare, FeatureLayer, Query, QueryTask, Multipoint,
             GeometryService, geometryEngine, BufferParameters) {
    return declare(null, {
        //CcObject properties
        layer: null,
        featureSet: null,

        /**
         * CcObject constructor: Constructs an object instance from either a Map Service or Feature Service
         * @param url: URL to the ArcGIS Server REST resource that represents an feature service.
         * @param opt: optional parameters (e.g. the SQL where clause to filter features).
         */
        constructor: function (url, opt) {
            if (url === null || url === "" || url === undefined) {
                console.error("Please enter a valid URL for the field data");
                return;
            }

            var featureLayer = new FeatureLayer({
                url: url
            });
            this.id = featureLayer.id;
            this.layer = featureLayer;

            if (opt !== undefined) {
                // Set definition expression in constructor to only display features that satisfy the SQL clause.
                if (opt.SQL !== undefined) {
                    this.layer.definitionExpression = opt.SQL;
                }
            }
            console.log("A CcObject instance was created.");
        },

        /**
         * CcObject function: returns true if two objects (with same CRS) are in a relationship of type relType.
         * @param obj: the other CcObject instance
         * @param relType: The spatial relationship to be tested between the two CcObject. Possible values include:
         *        contains | crosses | disjoint | equals | intersects | overlaps | relate| touches | within
         * Return type: Promise
         * Returns true if the relation of the input objects holds.
         */
        relation: function (obj, relType) {
            //get self CcObject's geometry
            return this.getGeometry()
                .then(getObjGeometry)
                .then(checkRelation);
            //get obj's geometry
            function getObjGeometry(g1) {
                return obj.getGeometry().then(function (g2) {
                    return [g1, g2];
                });
            }

            //check if the relationship exists between the two geometries
            function checkRelation(geoArray) {
                switch (relType) {
                    case "contains":
                        return geometryEngine.contains(geoArray[0], geoArray[1]);
                        break;
                    case "crosses":
                        // returns TRUE if the intersection results in a geometry that has a dimension
                        // that is one less than the maximum dimension of the two source geometries
                        // and the intersection set is interior to both source geometries.
                        return geometryEngine.crosses(geoArray[0], geoArray[1]);
                        break;
                    case "disjoint":
                        return geometryEngine.disjoint(geoArray[0], geoArray[1]);
                        break;
                    case "equals":
                        return geometryEngine.equals(geoArray[0], geoArray[1]);
                        break;
                    case "intersects":
                        return geometryEngine.intersects(geoArray[0], geoArray[1]);
                        break;
                    case "overlaps":
                        //overlaps returns TRUE only for geometries of the same dimension
                        // and only when their intersection set results in a geometry of the same dimension.
                        return geometryEngine.overlaps(geoArray[0], geoArray[1]);
                        break;
                    case "relate":
                        return geometryEngine.relate(geoArray[0], geoArray[1], "TT*TT****");
                        break;
                    case "touches":
                        return geometryEngine.touches(geoArray[0], geoArray[1]);
                        break;
                    case "within":
                        return geometryEngine.within(geoArray[0], geoArray[1]);
                        break;
                    default:
                        console.error(relType + " is not a valid value for relType parameter");
                        return;
                }
            }
        },

        /**
         * CcObject function: gets CcObject's bounds in form of a bounding box(xmin, ymin, xmax, ymax)
         * Return type: Promise
         * returns an Extent, which can be accessed using the .then() method once the promise resolves.
         */
        bounds: function () {
            var query = new Query();
            query.where = "1=1"; // Query for all records
            query.outFields = ["*"];
            query.returnGeometry = true;
            var process = this.layer.queryExtent(query);
            return process.then(function (extent) {
                return extent;
            });
        },

        /**
         * CcObject function: returns a property's value
         * @param prop: the property name
         * Return type: Promise
         * returns the value of the property when the promise resolves.
         */
        property: function (prop) {
            var query = this.layer.createQuery();
            query.outFields = ["*"];
            return this.layer.queryFeatures(query).then(function (featureSet) {
                return featureSet.features[0].attributes[prop];
            });
        },

        /**
         * CcObject function: checks whether two objects are same.
         * @param obj: the other CcObject instance
         * Return type: Boolean, returns true if the two objects have the same identity.
         */
        identity: function (obj) {
            return this.id === obj.id;
        },

        /**
         * CcObject function: gets CcObject's geometry (can be Point, Curve, Surface, or GeometryCollection)
         * Return type: Promise
         * Uses the callback function to receive the object's geometry.
         */
        getGeometry: function () {
            //var query = new Query();
            //if(this.layer.definitionExpression !== null){
            //    query.where = this.layer.definitionExpression;
            //}else{
            //    query.where = "1=1"; // Query for all records
            //}
            //query.outFields = ["*"];
            //query.returnGeometry = true;

            //var query = this.layer.createQuery();
            var lyr = this.layer;
            return this.layer.then(function () {
                return lyr.queryFeatures().then(function (featureSet) {
                    //Subclasses of Geometry in ArcGIS JavaScript API: Extent, Multipoint, Point, Polygon, and Polyline.
                    var geometry;
                    switch (featureSet.geometryType) {
                        case "polygon":
                            //A collection of rings ordered by their containment relationship.
                            //This may refer to Polygon or MultiPolygon in OGC terms
                            geometry = featureSet.features[0].geometry;
                            for (var i = 1; i < featureSet.features.length; i++) {
                                var rings = featureSet.features[i].geometry.rings;
                                for (var r = 0; r < rings.length; r++) {
                                    geometry.addRing(rings[r]);
                                }
                            }
                            break;
                        case "polyline":
                            //An ordered collection of paths.
                            //This may refer to LineRing or MultiLineRing in OGC terms
                            geometry = featureSet.features[0].geometry;
                            for (var i = 1; i < featureSet.features.length; i++) {
                                var paths = featureSet.features[i].geometry.paths;
                                for (var p = 0; p < paths.length; p++) {
                                    geometry.addPath(paths[p]);
                                }
                            }
                            break;
                        case "multipoint":
                            //An ordered collection of points.
                            geometry = featureSet.features[0].geometry;
                            for (var i = 1; i < featureSet.features.length; i++) {
                                var points = featureSet.features[i].geometry.points;
                                for (var p = 0; p < points.length; p++) {
                                    geometry.addPoint(points[p]);
                                }
                            }
                            break;
                        case "point":
                            if (featureSet.features.length > 1) {
                                var mp = new Multipoint();
                                for (var i = 0; i < featureSet.features.length; i++) {
                                    mp.addPoint(featureSet.features[i].geometry);
                                }
                            } else {
                                geometry = featureSet.features[0].geometry;
                            }
                            break;
                        case "extent":
                            //A rectangle indicating the spatial extent of another geometry.
                            break;
                        default:
                            console.log("This FeatureSet does not contain geometry");
                            return;
                    }
                    return geometry;
                });
            });
        },

        /**
         * CcObject function: Creates buffer polygons at a specified distance around the given object.
         * @param distance: the distance the input object are buffered.
         * @param unitType: the unit for calculating each buffer distance.(case insensitive: kilometer = Kilometer)
         *                 Units can be singular or plural forms: e.g. Foot = feet
         * Return type: Promise
         * Uses the callback function to receive the buffered polygon.
         */
        buffer: function (distance, unitType) {
            //This service provided by ESRI is for development and testing purposes only.
            //var gsUrl = "https://utility.arcgisonline.com/ArcGIS/rest/services/Geometry/GeometryServer";
            var gsUrl = "https://ags-raid.geog.ucsb.edu:6443/arcgis/rest/services/Utilities/Geometry/GeometryServer";
            var gs = new GeometryService(gsUrl);

            //Defines valid unit types here
            var bufferUnits = {
                "METER": GeometryService.UNIT_METER,
                "METERS": GeometryService.UNIT_METER,
                "KILOMETER": GeometryService.UNIT_KILOMETER,
                "KILOMETERS": GeometryService.UNIT_KILOMETER,
                "FOOT": GeometryService.UNIT_FOOT, //International foot (0.3048 meters)
                "FEET": GeometryService.UNIT_FOOT,
                "MILE": GeometryService.UNIT_STATUTE_MILE, //Miles (5,280 feet, 1,760 yards, or exactly 1,609.344 meters)
                "MILES": GeometryService.UNIT_STATUTE_MILE,
                "NAUTICAL_MILE": GeometryService.UNIT_NAUTICAL_MILE, //Nautical Miles (1,852 meters)
                "NAUTICAL_MILES": GeometryService.UNIT_NAUTICAL_MILE,
                "DEGREE": GeometryService.UNIT_DEGREE,
                "DEGREES": GeometryService.UNIT_DEGREE
            };

            //setup the buffer parameters
            var params = new BufferParameters();
            params.distances = [distance];
            params.unit = bufferUnits[unitType.toUpperCase()];
            //If true, all geometries buffered at a given distance are unioned into
            //a single (possibly multipart) polygon, and the unioned geometry is placed in the output array.
            params.unionResults = true;

            var process = this.getGeometry();
            return process.then(function (geom) {
                console.log("Doing the buffer...");
                //The Geometry Service can not buffer over 12500 (around 14000) features at one time.
                // The maxBufferCount property establishes the maximum number of features that can be buffered
                if (geom.type === "polyline" && geom.paths.length > 12500) {
                    var p1 = geom.paths.slice(0, 12500);
                    var g1 = geom.clone();
                    g1.paths = p1;
                    params.geometries = [g1];
                    //do the buffer
                    console.log("Buffering part 1...");
                    return gs.buffer(params).then(function (bufferedGeometries1) {
                        console.log("Buffering part 2...");
                        var p2 = geom.paths.slice(12500);
                        var g2 = geom.clone();
                        g2.paths = p2;
                        params.geometries = [g2];
                        var gs2 = new GeometryService("https://utility.arcgisonline.com/ArcGIS/rest/services/Geometry/GeometryServer");
                        return gs2.buffer(params).then(function (bufferedGeometries2) {
                            //console.log([bufferedGeometries1, bufferedGeometries2]);
                            //console.log(bufferedGeometries1.concat(bufferedGeometries2));
                            var gs3 = new GeometryService(gsUrl);
                            //constructs the set-theoretic union of the two buffered geometries
                            console.log("Unifying two parts...");
                            //union function returns a "<Geometry> geometry" Object, then converts it to an Array[1]
                            return gs3.union(bufferedGeometries1.concat(bufferedGeometries2)).then(function (geoUnion) {
                                console.log("buffer finished!");
                                return geoUnion;
                            });
                        });
                    });
                } else {
                    params.geometries = [geom];
                    //GeometryService buffer function returns a "<Polygon[]> geometries" Array[1],
                    // so just return the first element: "Polygon".
                    return gs.buffer(params).then(function (polygonArray) {
                        return polygonArray[0];
                    });
                }

                /**
                 * The GeometryEngine has two methods for buffering geometries client-side: buffer and geodesicBuffer.
                 * Use caution when deciding which method to use. As a general rule, (1) use geodesicBuffer if the
                 * input geometries have a spatial reference of either WGS84 (wkid: 4326) or Web Mercator;
                 * (2) use GeometryService.buffer() if you need to buffer geometries
                 *     with a geographic coordinate system other than WGS84 (wkid: 4326);
                 * (3) Only use buffer when attempting to buffer geometries
                 *     with a projected coordinate system other than Web Mercator.
                 */
                //if(geom.spatialReference.isWGS84 || geom.spatialReference.isWebMercator){
                //    //WGS84 (wkid: 4326) or Web Mercator
                //    return geometryEngine.geodesicBuffer(geom, distance, unitType);
                //}else if (geom.spatialReference.isGeographic){
                //    //geometries with a geographic coordinate system other than WGS84 (wkid: 4326)
                //    return gs.buffer(params).then(function (polygonArray) {
                //        return polygonArray[0];
                //    });
                //}else{
                //    //geometries with a projected coordinate system other than Web Mercator
                //    return geometryEngine.buffer(geom, distance, unitType);
                //}
            });
        }
    });
});