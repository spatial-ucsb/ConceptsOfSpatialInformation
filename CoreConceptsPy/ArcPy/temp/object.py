import os

from coreconcepts import CcObject


class ArcShpObject(CcObject):
    """
    Concrete class for core concept 'object'
    For handling .shp files
    """

    def __init__(self, filepath, obj_index, domain):
        super(ArcShpObject, self).__init__(filepath, obj_index, domain)
        self.filepath = filepath
        self.sObj = obj_index
        self.domain = domain
        self.filename = os.path.basename(filepath)

    def buffer(self, object, distance):
        """
        Buffer input object
        @param object an object to buffer
        @param distance a distance extent to buffer
        """
        output = arcpy.Buffer_analysis(self.filename, object.filenameFull)
        # TODO: implement saving and updating credentials (see other methods)
        raise NotImplementedError("buffer")


    def relation( self, obj, rel_type ):
        pass

    def bounds( self ):
        pass

    def property( self, prop ):
        pass

    def identity( self, obj ):
    pass
