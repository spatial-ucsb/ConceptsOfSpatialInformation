import os
from coreconcepts import CcObject

class ArcShpObject(CcObject):
    """
    Concrete class for core concept 'object'
    For handling .shp files
    """
    def __init__( self, filepath, objIndex, domain ):
        super(ArcShpObject, self).__init__(filepath, objIndex, domain)
        self.filepath = filepath
        self.sObj = objIndex
        self.domain = domain
        self.filename = os.path.basename(filepath)

    def buffer ( self, distance, unitType ):
        """
        Buffer input object
        @param distance a distance extent to buffer
        @param unitType unit type (ie. decimal degrees, feet)
        """

        outcome = "\_buffer_"
        # determine save file path
        outputLocation = self.filepath + outcome + self.filename

        # calculate buffer
        concatDistance = str(distance) + " " + unitType
        arcpy.Buffer_analysis(self.filename, outputLocation, concatDistance)

        # update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self

    def relation( self, obj, rel_type ):
        raise NotImplementedError("relation")

    def bounds( self ):
        raise NotImplementedError("bounds")

    def property( self, prop ):
        raise NotImplementedError("property")

    def identity( self, obj ):
        raise NotImplementedError("identity")
