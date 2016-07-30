# make CcField instance (factory)
from field import GeoTiffField
from object import ArcShpObject

from arcpy import Describe


def make_field(filepath):
    """
    :param filepath: data source file path
    :return: new Ccfield instance
    """
    domain = determine_domain(filepath)  # determine domain
    # determine input file type
    if filepath.endswith(".tif"):
        return GeoTiffField(filepath, domain)
    elif filepath.endswith(".mp3"):
        pass
    assert 0, "Bad shape creation: " + filepath


def make_object(filepath):
    """
    :param filepath: data source file path
    :return: new Ccobject instance
    """
    domain = determine_domain(filepath)  # determine domain
    # determine input file type
    if filepath.endswith(".shp"):
        return ArcShpObject(filepath, 1, domain)  # TODO: alter objIndex
    elif filepath.endswith(".mp3"):
        pass
    assert 0, "Bad shape creation: " + filepath


def determine_domain(filepath):
    """
    :param filepath: data source filepath
    :return: ArcPy domain extent
    """
    desc = arcpy.Describe(filepath)
    return desc.extent

# TODO: Integrate geoEvent & other cc elements into instance creation
# TODO: Refactor code via methods mentioned in other TODOs (separate by file; determine imports)
