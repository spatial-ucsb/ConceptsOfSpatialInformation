/**
 * JavaScript implementation of the core concept 'field'.
 * The implementation has migrated from ArcGIS JavaScript API 3.x to 4.x
 * The constructor was refactored to support "overloading".
 * version: 2.0.0
 * (c) Liangcun Jiang
 * latest change: July 25, 2017.
 */
define([
    "dojo/_base/declare",
    "esri/layers/ImageryLayer",
    "esri/layers/support/RasterFunction",
    "esri/layers/support/DimensionalDefinition",
    "esri/layers/support/MosaicRule",
    "dojo/domReady!"
], function (declare, ImageryLayer, RasterFunction, DimensionalDefinition, MosaicRule) {
    //null signifies that this class has no classes to inherit from
    return declare(null, {
        /**
         *Field constructor: Constructs a field instance from an image service
         *@param url: The URL to the REST endpoint of an image service either on ArcGIS for Server, Portal for ArcGIS, or ArcGIS Online.
         *@param opt: optional parameters including the domain and granularity of a field instance
         */
        constructor: function (url, opt) {
            if (url === null || url === "" || url === undefined) {
                console.error("Invalid URL for the field data");
                return;
            }
            //default rending rule is "None"
            var rf = new RasterFunction({
                functionName: "Stretch",
                functionArguments: {
                    "StretchType": 0
                }
            });
            this._rule = rf;

            if (opt !== undefined) {

                //set domain property
                if (opt.domain !== undefined) {
                    this._domain = opt.domain;
                    var ins = opt.domain.inside;
                    if (ins !== undefined && ins !== null) {
                        for (var i = 0; i < ins.length; i++) {
                            var rfClip = new RasterFunction();
                            rfClip.functionName = "Clip";
                            var functionArguments = {};
                            //int (1= clippingOutside, 2=clippingInside), use 1 to keep image inside of the geometry
                            functionArguments.ClippingType = 1;
                            functionArguments.ClippingGeometry = ins[i];
                            functionArguments.Raster = this._rule;
                            rfClip.functionArguments = functionArguments;
                            this._rule = rfClip;
                        }
                    }
                    var outs = opt.domain.outside;
                    if (outs !== undefined && outs !== null) {
                        for (var i = 0; i < outs.length; i++) {
                            var rfClip = new RasterFunction();
                            rfClip.functionName = "Clip";
                            var functionArguments = {};
                            //int (1= clippingOutside, 2=clippingInside), use 1 to keep image inside of the geometry
                            functionArguments.ClippingType = 2;
                            functionArguments.ClippingGeometry = outs[i];
                            functionArguments.Raster = this._rule;
                            rfClip.functionArguments = functionArguments;
                            this._rule = rfClip;
                        }
                    }
                }

                //set granularity property
                if (opt.granularity !== undefined) {
                    this._granularity = opt.granularity;

                    var rfResample = new RasterFunction();
                    rfResample.functionName = "Resample";
                    //rfResample.variableName = "Raster";
                    var functionArguments = {};
                    // ResamplingType: 0=NearestNeighbor,2=Cubic,3=Majority,
                    // 1=Bilinear, 4=BilinearInterpolationPlus, 5=BilinearGaussBlur,
                    // 6=BilinearGaussBlurPlus, 7=Average, 8=Minimum, 9=Maximum,10=VectorAverage(require two bands)
                    functionArguments.ResamplingType = 1;
                    functionArguments.InputCellsize = {"x": opt.granularity[0], "y": opt.granularity[1]};
                    functionArguments.Raster = this._rule;
                    rfResample.functionArguments = functionArguments;
                    this._rule = rfResample;
                }

                //additional mosaic rule
                if (opt.dimInfo !== undefined) {
                    var dimInfo = opt.dimInfo; //json object
                    var x;
                    var dd = [];
                    for (x in dimInfo) {
                        dd.push(new DimensionalDefinition({
                            dimensionName: x,
                            values: [dimInfo[x]],
                            isSlice: true
                        }));
                    }
                    var mr = new MosaicRule({
                        multidimensionalDefinition: dd
                    });
                    this._mosaicRule = mr;
                }
            }

            var imageLayer = new ImageryLayer({
                url: url,
                renderingRule: this._rule,
                mosaicRule: this._mosaicRule
            });

            this.layer = imageLayer;
            if (!this._domain) {
                this._domain = {inside: [imageLayer.fullExtent], outside: []};
            }
        },

        /**
         *Field function: Gets field's domain
         */
        domain: function () {
            return this._domain;
        },

        /**
         *Field function: Restricts current field's domain
         *@param geometry: a geometry applied to the current domain
         *@param type: operation type can be either "inside" or "outside"
         */
        restrictDomain: function (geometry, type) {
            if (type !== "inside" && type !== "outside") {
                console.error("Invalid or missing input parameters for restrictDomain function");
                return;
            }
            (type === "inside") ? this._domain.inside.push(geometry) : this._domain.outside.push(geometry);

            var rfClip = new RasterFunction();
            rfClip.functionName = "Clip";
            //rfClip.variableName = "Raster";
            var functionArguments = {};
            //int (1= clippingOutside, 2=clippingInside), use 1 to keep image inside of the geometry
            functionArguments.ClippingType = (type === "inside" ? 1 : 2);
            functionArguments.ClippingGeometry = geometry;
            functionArguments.Raster = this._rule;
            rfClip.functionArguments = functionArguments;
            this._rule = rfClip;
            this.layer.renderingRule = this._rule;
            console.log("restrictDomain operation was invoked!");
        },

        /**
         * Field function: Performs bitwise, conditional, logical, mathematical,
         * and statistical operations on a pixel-by-pixel basis.
         *@param field: another field or a scalar/number
         *@param operation: valid option -- "average", "max", "min", "plus", "minus" (extended as needed)
         */
        local: function (field, operation) {
            //Operations: 1 = Plus, 2 = Minus, 3 = Times, 67= MaxIgnoreNoData, 68 = MeanIgnoreNoData, 70 = MinIgnoreNoData,
            //23 = Divide ...
            //http://resources.arcgis.com/en/help/arcobjects-net/componenthelp/index.html#//004000000149000000
            //Defines valid local operations here
            var ops = {
                "average": 68,
                "plus": 1,
                "minus": 2,
                "max": 67,
                "min": 70
            };
            if (!(operation in ops)) {
                console.error("Invalid or missing input parameters for local function.");
                return;
            }

            var rfLocal = new RasterFunction();
            rfLocal.functionName = "Local";
            //rfLocal.variableName = "Rasters";
            var functionArguments = {};
            functionArguments.Operation = ops[operation];
            if (isNaN(field)) {
                //if the input is Not a Number
                functionArguments.Rasters = [this._rule, field._rule];
            } else {
                //if the input is a number/scalar
                functionArguments.Rasters = [this._rule, field];
            }
            rfLocal.functionArguments = functionArguments;
            this._rule = rfLocal;
            this.layer.renderingRule = this._rule;
            console.log("local operation was invoked!");
        },

        /**
         * Field function: calculates focal statistics for each pixel of an image based on a defined focal neighborhood.
         *@param kernelColumns: defines neighbour by columns, it should be an int (e.g. 3)
         *@param kernelRows: defines neighbour by rows, it should be an int (e.g. 3)
         *@param type: Min | Max | Mean | StandardDeviation
         */
        focal: function (kernelColumns, kernelRows, type) {
            //1=Min, 2=Max, 3=Mean, 4=StandardDeviation
            var ops = {
                "Min": 1,
                "Max": 2,
                "Mean": 3,
                "StandardDeviation": 4
            };
            if (!(type in ops)) {
                console.error("Invalid type parameters for focal function.");
                return;
            }
            var rfFocal = new RasterFunction();
            rfFocal.functionName = "Statistics";
            rfFocal.variableName = "Rasters";
            var functionArguments = {
                "Type": ops[type],
                "KernelColumns": kernelColumns,
                "KernelRows": kernelRows
            };
            rfFocal.functionArguments = functionArguments;
            this._rule = rfFocal;
            this.layer.renderingRule = this._rule;
        },

        /**
         * Field function: Resamples pixel values to a lower granularity
         *@param cellW: cell width
         *@param cellH: cell height
         */
        coarsen: function (cellW, cellH) {
            var rfResample = new RasterFunction();
            rfResample.functionName = "Resample";
            //rfResample.variableName = "Raster";
            var functionArguments = {};
            // ResamplingType: 0=NearestNeighbor,2=Cubic,3=Majority,
            // 1=Bilinear, 4=BilinearInterpolationPlus, 5=BilinearGaussBlur,
            // 6=BilinearGaussBlurPlus, 7=Average, 8=Minimum, 9=Maximum,10=VectorAverage(require two bands)
            functionArguments.ResamplingType = 1;
            functionArguments.InputCellsize = {"x": cellW, "y": cellH};
            functionArguments.Raster = this._rule;
            rfResample.functionArguments = functionArguments;
            this._rule = rfResample;
            this.layer.renderingRule = this._rule;
            console.log("coarsen operation was invoked!");
        }
    });
});
