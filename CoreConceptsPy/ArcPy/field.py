import os

from coreconcepts import CcField


class GeoTiffField(CcField):
    """
    Concrete class for core concept 'field'
    For handling .tiff files
    """

    def __init__(self, filepath, geo_object):
        super(GeoTiffField, self).__init__(filepath, geo_object)  # TODO: check if syntax is correct for returning type (make sure __init__ is correct)
        self.filepath = filepath
        self.domain = geo_object
        self.filename = os.path.basename(filepath)

    def value_at(self, value_at):
        # TODO: return value at current position (must integrate with other operations)
        raise NotImplementedError("value at")

    def domain(self):
        return super

    def restrict_domain(self, domain_obj, operation):
        """
        Restricts current instance's domain based on object's domain
        @param domain_obj an object to be subtracted to the current domain
        @param operation an operation to be performed based on the object
        """
        if operation == 'inside':
            # arcpy.env.snapRaster = self.filepath #TODO: will resolve output shift

            # extract by mask
            output = arcpy.sa.ExtractByMask(self.filename, domain_obj.filename)
            # determine save credentials
            (nfilepath, nfilename) = os.path.split(self.filepath)
            outputLocation = nfilepath + "\_masked_" + nfilename
            output.save(outputLocation)

            # and update cc instance's attributes
            desc = arcpy.Describe(outputLocation)
            self.domain = desc.extent
            self.filepath = outputLocation
            self.filename = os.path.basename(outputLocation)
        elif operation == 'ouside':
            # TODO: implement outside computations (similar to erase)
            raise NotImplementedError("restrict domain 'outside'")
            pass

        # TODO: return 'self'

    def local(self, fields, operation):  # TODO: fields is a list, make it one
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
        elif operation == 'maximum':
            # TODO complete list of local operations
            # output = (Float(self.filepath)+Float(fields.filepath))/2
            raise NotImplementedError("local 'maximum'")

        else:
            print 'the input function is not defined'

        #return output

