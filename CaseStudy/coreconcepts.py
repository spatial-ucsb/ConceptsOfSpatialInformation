# -*- coding: utf-8 -*-
import os

# TODO: refactor so that following arc implementations aren't called unless arc processing is needed
import arcpy
from arcpy import env
from arcpy.sa import *

# Set ArcPy workspace settings
env.workspace = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data" # TODO: set workspace determined by filepath locations
workspace = env.workspace
arcpy.env.overwriteOutput = True
# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")


##############################
## Core Concepts classes ##


class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """
    def __init__(self, filepath, geoObject):
        self.filepath = filepath
        self.domain = geoObject
        # TODO: restrict value pairs to geoObject
        pass


    def value_at( self, position ):
        """
        @return the value of field at position, or None if it is outside of the domain.
        """
        # TODO: check if position falls within value
        raise NotImplementedError("valueAt")


    def domain( self ):
        """
        @return current domain of the field
        """
        raise NotImplementedError("domain")


    def restrict_domain(self, object, operation ):
        pass


    def local( self, fields, fun ):
        """
        Uses raster calculator from ArcPy
        TODO: make a general funtion for more than two fields
        """
        raise NotImplementedError("local")


class CcObject(object):
    """
    Abstract class for core concept 'object'
    Based on Object.hs
    """
    def __init__( self, filepath, objIndex, geoObject ):
        self.filepath = filepath
        self.sObj = objIndex
        self.domain = geoObject


    def bounds( self ):
        raise NotImplementedError("bounds")


    def relation( self, obj, relType ):
        """ @return Boolean True if self and obj are in a relationship of type relType
                    False otherwise
        """
        raise NotImplementedError("relation")


    def property( self, prop ):
        """
        @param prop the property name
        @return value of property in obj
        """
        raise NotImplementedError("property")


    def identity( self, obj ):
        """
        @param an object
        @return Boolean True if self and obj are identical
        """
        raise NotImplementedError("identity")


class CcGranularity:
    def __init__(self):
        # TODO: cell_size_x, cell_size_y
        raise NotImplementedError("CcGranularity")


##############################
## Core Concepts Subclasses ##


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


    def restrict_domain(self, object, operation ):
        """
        Restricts current instance's domain based on object's domain
        @param object an object to be subtracted to the current domain
        @param operation on object, valid options: "inside", "outside"
        """

        (nfilepath, nfilename) = os.path.split(self.filepath)
        outputLocation = "-"

        if operation == 'inside':
            ## arcpy.env.snapRaster = self.filepath #TODO: resolve output shift
            # extract by mask
            output = arcpy.sa.ExtractByMask(self.filename, object.filename)
            # determine save credentials
            outputLocation = nfilepath + "\_masked_" + nfilename
            output.save(outputLocation)

        elif operation == 'outside':
            # "preprocessing" temporary 'fix' to create China w/o gas flares (needed for Extract By Mask)
            newChina = self.removeFlares(object)

            print("output location2 ", newChina)
            # extract by mask
            output = arcpy.sa.ExtractByMask(self.filename, newChina)
            # determine save credentials
            outputLocation = nfilepath + "\_erased_" + nfilename
            output.save(outputLocation)
            print("output location ", outputLocation)

            ## raise NotImplementedError("restrict domain 'outside'")
            ## pass

        # update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        print("self type: ", type(self))

        return self

    # TODO: remove; temporary fix to "preprocess"; see restrict_domain
    def removeFlares(self, object):
        outputLocation = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\China_noFlares.shp"
        # erase gas flares from country, generates a mask
        arcpy.Erase_analysis(r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\China.shp", object.filename, outputLocation)

        return outputLocation


    def local( self, fields, operation ): # TODO: fields is a list, make it one
        """
        Uses raster calculator from ArcPy
        @param fields a field to be subtracted to the current domain
        @param operation an operation to be performed based on the field
        """
        if operation == 'average':
            # perform averaging operation # TODO: generalize funtion for more than two fields
            output = (Float(self.filepath)+ Float(fields.filepath))/2
            # determine save credentials
            (nfilepath, nfilename) = os.path.split(self.filepath)
            outputLocation = nfilepath + "\_averaged" + nfilename
            output.save(outputLocation)

            # and update cc instance's attributes
            desc = arcpy.Describe(outputLocation)
            self.domain = desc.extent
            self.filepath = outputLocation
            self.filename = os.path.basename(outputLocation)

            print("self.domain ", self.domain)
            print("self.filepath ", self.filepath)
            print("self.filename ", self.filename)
        elif operation == 'maximum':
            #TODO complete list of local operations
            #output = (Float(self.filepath)+Float(fields.filepath))/2
            raise NotImplementedError("local 'maximum'")

        else:
            print 'the input function is not defined'

        return self


    def coarsen( self, cellW, cellH ):
        """
        Uses resample from Data Management in ArcPy
        @param cellW cell width
        @param callH cell height
        """
        (nfilepath, nfilename) = os.path.split(self.filepath)
        outputLocation = nfilepath + "\_coarsened" + nfilename

        concatCellSize = str(cellW) + " " + str(cellH)

        arcpy.Resample_management(self.filename, outputLocation, concatCellSize)

        # and update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self

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

        (nfilepath, nfilename) = os.path.split(self.filepath)
        outputLocation = nfilepath + "\_buffered_" + nfilename

        concatDistance = str(distance) + " " + unitType
        arcpy.Buffer_analysis(self.filename, outputLocation, concatDistance)

        # update cc instance's attributes
        desc = arcpy.Describe(outputLocation)
        self.domain = desc.extent
        self.filepath = outputLocation
        self.filename = os.path.basename(outputLocation)

        return self



#######################
## Utility functions ##


# make CcField instance (factory)
def makeField(filepath):
    try:
        domain = determineDomain(filepath) # determine domain
        # determine input file type
        if filepath.endswith(".tif"):
            return GeoTiffField(filepath, domain)
        elif filepath.endswith(".mp3"):
            pass
        #makeField = staticmethod(makeField)
    except IOError as e:
        print "Cannot make object. The file type at " + filepath + " is not a valid type"


# make CcObject instance (factory)
def makeObject(filepath):
    try:
        domain = determineDomain(filepath) # determine domain
        # determine input file type
        if filepath.endswith(".shp"):
            return ArcShpObject(filepath, 1, domain) #TODO: alter objIndex
        elif filepath.endswith(".mp3"):
            pass
        #makeObject = staticmethod(makeObject)
    except IOError as e:
        print "Cannot make object. The file type at " + filepath + " is not a valid type"


# helper function for cc factories
def determineDomain(filepath):
    desc = arcpy.Describe(filepath)
    return desc.extent

# TODO: Integrate geoEvent & other cc elements into instance creation
# TODO: Refactor code via methods mentioned in other TODOs (separate by file; determine imports)
