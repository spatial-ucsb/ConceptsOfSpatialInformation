import os
from coreconcepts import CcField

class GeoTiffField(CcField):
    """
    Concrete class for core concept 'field'
    For handling .tiff files
    """

    def __init__(self, filepath, geoObject):
        super(GeoTiffField, self).__init__(filepath, geoObject) # TODO: check if syntax is correct for returning type (make sure __init__ is correct)
        self.filepath = filepath
        self.domain = geoObject
        self.filename = os.path.basename(filepath)

    def value_at(self, value_at):
        # TODO: return value at current position (must integrate with other operations)
        raise NotImplementedError("value at")

    def domain(self):
        return self.domain

    def restrict_domain(self, object, operation):
        """
        Restricts current instance's domain based on object's domain
        @param object an object to be subtracted to the current domain
        @param operation on object, valid options: "inside", "outside"
        """

        operation = "\_operation_"

        if operation == 'inside':
            ## arcpy.env.snapRaster = self.filepath
            # TODO: resolve output shift

            # extract by mask
            output = arcpy.sa.ExtractByMask(self.filename, object.filename)
            outcome = "\_inside_"

        elif operation == 'outside':
            # TODO: refactor erasing
            eraseLocation = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\China_noFlares.shp"
            # erase gas flares from country, generates a mask
            arcpy.Erase_analysis(r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\China.shp", object.filename, eraseLocation)

            # extract by mask
            output = arcpy.sa.ExtractByMask(self.filename, newChina)
            outcome = "\_outside_"

        else:
            raise NotImplementedError(operation)

        # determine save credentials
        outputLocation = self.filepath + outcome + self.filename
        output.save(outputLocation)

        # update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self

    def local( self, fields, operation ): # TODO: fields is a list, make it one
        """
        Uses raster calculator local operation from ArcPy
        @param fields a field to be subtracted to the current domain
        @param operation an operation to be performed based on the field
        """
        if operation == 'average':
            # perform averaging operation
            output = (Float(self.filepath) + Float(fields.filepath)/len(fields))
            outcome = "\_average_"

        elif operation == 'maximum':
            #TODO complete list of local operations
            #output = (Float(self.filepath)+Float(fields.filepath))/2
            raise NotImplementedError("local 'maximum'")

        else:
            raise NotImplementedError(operation)

        # determine save credentials
        outputLocation = self.filepath + outcome + self.filename
        output.save(outputLocation)

        # and update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self


    def coarsen( self, cellW, cellH ):
        """
        Uses resample from Data Management in ArcPy
        @param cellW cell width
        @param callH cell height
        """

        # determine save credentials
        outcome = "\_coarsen_"
        outputLocation = self.filepath + outcome + self.filename

        concatCellSize = str(cellW) + " " + str(cellH)

        arcpy.Resample_management(self.filename, outputLocation, concatCellSize)

        # and update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self
