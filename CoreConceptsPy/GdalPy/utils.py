#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utils: Various utilities methods.
"""
__author__ = "Andrea Ballatore"
__copyright__ = "Copyright 2014"
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import logging
import math
import re

def _init_log(module_name):
    assert module_name
    return logging.getLogger(module_name)

log = _init_log("utils")

def _json_pretty_print( jsonObj ):
    s = json.dumps(jsonObj, indent=3, sort_keys=True)
    return s

def _to_unicode(s):
    if (type(s) is str):
        try:
            return unicode(s)
            #return s
        except UnicodeDecodeError:
            #print "UnicodeDecodeError on string: "+s
            return s
    else: return s

def _read_file( filePath ):
    """ Loads file into a string """
    with open (filePath, "r") as f:
        res = f.read()#.replace('\n', '')
        return res
    return None

def _is_str(*objs):
    """ Checks if objs are strings """
    for i in range(len(objs)):
        b = (type(objs[i]) is str) or (type(objs[i]) is unicode)
        if not b: return False
    return True

def _is_nan(*objs):
    """ Checks if objs are not-a-number """
    for i in range(len(objs)):
        b = math.isnan(objs[i])
        if not b: return False
    return True

def _is_number(*objs):
    """ Checks if objs are numbers """
    for i in range(len(objs)):
        b = isinstance(objs[i], (int, long, float, complex))
        if not b: return False
    return True

def _write_str_to_file( s, fn ):
    assert _is_str(s,fn)
    with open(fn, "w") as text_file: text_file.write(s)
    log.info(str(len(s))+" chars written in "+fn)

def _wrap_cdata_text( s ):
    ss = "<![CDATA[\n" + s + "\n]]>"
    return ss

def _read_str_from_file( fn ):
    content = False
    with open(fn) as f:
        content = f.readlines()
    return "".join(content)

def _cut_str( s, maxchar ):
    if s is None: return s
    assert _is_str(s)
    if len(s)>maxchar: return s[:maxchar]+"..."
    else: return s

def _get_ellipse_coords( x, y, a, b, angle=0.0, k=2):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts = np.zeros((360*k+1, 2))

    beta = -angle * np.pi/180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j*(360*k+1)])

    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)

    pts[:, 0] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts[:, 1] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts

def _sort_dict_by_value(d, asc=True):
    s = sorted(d.items(), key=itemgetter(1), reverse=not asc)
    return s

def _valid_XML_char_ordinal(i):
    return ( # conditions ordered by presumed frequency
        0x20 <= i <= 0xD7FF
        or i in (0x9, 0xA, 0xD)
        or 0xE000 <= i <= 0xFFFD
        or 0x10000 <= i <= 0x10FFFF
        )

def _clean_str_for_xml( s ):
    clean_s = ''.join(c for c in s if _valid_XML_char_ordinal(ord(c)))
    #print clean_s
    clean_s = clean_s.decode('utf-8')
    #print clean_s
    return clean_s

def _str_to_ascii( a ):
    """
    Decode any string to ASCII.
    This avoids many unicode problems, but loses non English characters.
    @param a a string
    @return an ASCII string
    """
    assert _is_str(a)
    return a.decode('ascii', 'ignore')

def _split_list(alist, wanted_parts):
    length = len(alist)
    sublists = [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]
    i = 0
    for s in sublists: i+=len(s)
    assert i == len(alist)
    return sublists

def float_eq( a, b, err=1e-08):
    """
    Check if floats a and b are equal within tolerance err
    @return boolean
    """
    return abs(a - b) <= err


"""
Utility functions for fields.py
"""
def _pixel_to_coords(col, row, transform):
    """Returns the geographic coordinate pair (lon, lat) for the given col, row, and geotransform."""

    lon = transform[0] + (col * transform[1]) + (row * transform[2])
    lat = transform[3] + (col * transform[4]) + (row * transform[2])

    return lon, lat

def _coords_to_pixel(y, x, transform):
    """Returns raster coordinate pair (col, row) for the given lon, lat, and geotransform."""

    col = int((y - transform[0]) / transform[1])
    row = int((x - transform[3]) / transform[5])

    return col, row

def _rasterize_layer(layer, reference=None, ncols=None, nrows=None, projection=None, transform=None):
    """Returns a 2d numpy array of the rasterized layer."""

    import gdal, fields

    if isinstance(reference, gdal.Dataset):
        ncols = reference.RasterYSize
        nrows = reference.RasterXSize
        projection = reference.GetProjection()
        transform = reference.GetGeoTransform()
    elif isinstance(reference, fields.GeoTiffField):
        nrows, ncols = reference.data.shape
        projection = reference.projection
        transform = reference.transform
    elif not all([ncols, nrows, projection, transform]):
        raise ValueError("Must specify either a reference raster/field or pass the nrows, ncols, projection, and transform parameters.")

    raster = gdal.GetDriverByName('MEM').Create('', ncols, nrows, 1, gdal.GDT_Byte)
    raster.SetProjection(projection)
    raster.SetGeoTransform(transform)
    raster.GetRasterBand(1).Fill(0)

    gdal.RasterizeLayer(raster, [1], layer, None, None, [1], ['ALL_TOUCHED=TRUE'])

    return raster.ReadAsArray()