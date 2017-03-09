/**
 * JavaScript implementation of the core concept 'field'
 * version: 0.3.1
 * (c) Liangcun Jiang
 * latest change: March 8, 2017.
 */
define([
    "dojo/_base/declare",
    "esri/layers/ArcGISImageServiceLayer",
    "esri/tasks/query",
    "esri/layers/FeatureLayer",
    "esri/layers/ImageServiceParameters",
    "esri/layers/RasterFunction",
    "dojo/domReady!"
], function (declare,
             ArcGISImageServiceLayer,
             Query,
             FeatureLayer,
             ImageServiceParameters,
             RasterFunction) {
    //null signifies that this class has no classes to inherit from
    return declare(null, {
        /**
         *Field constructor: Constructs a field instance from an image service
         *@param url: URL to the ArcGIS Server REST resource that represents an image service.
         */
        constructor: function (url) {
            if (url === null || url === "" || url === undefined) {
                console.error("Please enter a valid URL for the field data");
                return;
            }
            var rf = new RasterFunction();
            rf.functionName = "Stretch";
            //StretchType: 0 = None, 3 = StandardDeviation, 4 = Histogram Equalization,
            // 5 = MinMax, 6 = PercentClip, 9 = Sigmoid
            rf.functionArguments = {
                "StretchType": 9, //9 = Sigmoid
                "UseGamma": true,
                "ComputeGamma": true,
                "DRA": true
            };
            //rf.functionArguments = {
            //    "StretchType": 0
            //};
            //rf.functionArguments = {
            //    "StretchType": 6, //6 = PercentClip
            //    "MinPercent": 0.5,
            //    "MaxPercent": 0.5,
            //    "UseGamma": true,
            //    "ComputeGamma": true,
            //    //"Gamma": [3.81464485861804, 3.81464485861804, 3.81464485861804],
            //    "DRA": true
            //};
            var params = new ImageServiceParameters();
            params.renderingRule = rf;

            var imageLayer = new ArcGISImageServiceLayer(url, {imageServiceParameters: params});
            this.layer = imageLayer;
            this.rasterFunction = rf;
            this.domain = {"inside": [], "outside": []};
            console.log("A CcField instance was created.");
        },

        getDomain: function () {
            return this.domain;
        },

        /**
         *Field function: Restricts current field's domain based on object's domain
         *@param geometry: a geometry applied to the current domain
         *@param type: operation type on object, can be either "inside" or "outside"
         */
        restrictDomain: function (geometry, type) {
            if (type !== "inside" && type !== "outside") {
                console.error("Invalid or missing input parameters for restrictDomain function");
                return;
            }
            (type === "inside") ? this.domain.inside.push(geometry) : this.domain.outside.push(geometry);

            var rfClip = new RasterFunction();
            rfClip.functionName = "Clip";
            rfClip.variableName = "Raster";
            var functionArguments = {};
            //int (1= clippingOutside, 2=clippingInside), use 1 to keep image inside of the geometry
            functionArguments.ClippingType = (type === "inside" ? 1 : 2);
            functionArguments.ClippingGeometry = geometry;
            functionArguments.Raster = this.rasterFunction;
            rfClip.functionArguments = functionArguments;
            this.rasterFunction = rfClip;
            //this.layer.setRenderingRule(this.rasterFunction);
            console.log("restrictDomain operation was invoked!");
        },

        /**
         * Field function: Performs bitwise, conditional, logical, mathematical,
         * and statistical operations on a pixel-by-pixel basis.
         *@param field: another field or a scalar/number
         *@param operation: valid option -- "average", "max", "min", "plus", "minus" (extended as needed)
         */
        local: function (field, operation) {
            //Operations: 1 = Plus, 2 = Minus, 3 = Times, 67= MaxIgnoreNoData, 70 = MinIgnoreNoData,
            //23 = Divide ..., 68 = MeanIgnoreNoData(extremely time-consuming)
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
            rfLocal.variableName = "Rasters";
            var functionArguments = {};
            functionArguments.Operation = ops[operation];
            if (isNaN(field)) {
                //if the input is Not a Number
                functionArguments.Rasters = [this.rasterFunction, field.rasterFunction];
            } else {
                //if the input is a number/scalar
                functionArguments.Rasters = [this.rasterFunction, field];
            }
            rfLocal.functionArguments = functionArguments;

            this.rasterFunction = rfLocal;
            //this.layer.setRenderingRule(rfLocal);
            console.log("local operation was invoked!");
        },

        /**
         * Field function: calculates focal statistics for each pixel of an image based on a defined focal neighborhood.
         *@param kernelColumns: defines neighbour by columns, it should be an int (e.g. 3)
         *@param kernelRows: defines neighbour by rows, it should be an int (e.g. 3)
         *@param type: Min | Max | Mean | StandardDeviation
         */
        focal: function (kernelColumns, kernelRows, type) {
            var rfFocal = new RasterFunction();
            rfFocal.functionName = "Local";
            rfFocal.variableName = "Rasters";
            var functionArguments = {
                "Type": type,
                "KernelColumns": kernelColumns,
                "KernelRows": kernelRows
            };
            this.rasterFunction = rfFocal;
            //this.layer.setRenderingRule(rfFocal);
        },

        /**
         * Field function: Resamples pixel values to a lower granularity
         *@param cellW: cell width
         *@param callH: cell height
         */
        coarsen: function (cellW, cellH) {
            var rfResample = new RasterFunction();
            rfResample.functionName = "Resample";
            rfResample.variableName = "Raster";
            var functionArguments = {};
            // ResamplingType: 0=NearestNeighbor,2=Cubic,3=Majority,
            // 1=Bilinear, 4=BilinearInterpolationPlus, 5=BilinearGaussBlur,
            // 6=BilinearGaussBlurPlus, 7=Average, 8=Minimum, 9=Maximum,10=VectorAverage(require two bands)
            functionArguments.ResamplingType = 0;
            functionArguments.InputCellsize = {"x": cellW, "y": cellH};
            functionArguments.Raster = this.rasterFunction;
            rfResample.functionArguments = functionArguments;
            this.rasterFunction = rfResample;
            //this.layer.setRenderingRule(rfResample);
            console.log("coarsen operation was invoked!");
        },

        /**
         * refreshes the field according to its current render rule.
         */
        show: function () {
            this.layer.setRenderingRule(this.rasterFunction);
            console.log("CcField was refreshed.");
        }
    });
});
