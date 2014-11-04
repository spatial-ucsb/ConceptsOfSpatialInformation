#!/usr/bin/env python

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
    with open (filePath, "r") as f:
        res = f.read()#.replace('\n', '')
        return res
    return None

def _is_str(*objs):
    for i in range(len(objs)):
        b = (type(objs[i]) is str) or (type(objs[i]) is unicode)
        if not b: return False
    return True

def _is_nan(*objs):
    for i in range(len(objs)):
        b = math.isnan(objs[i])
        if not b: return False
    return True

def _is_number(*objs):
    for i in range(len(objs)):
        b = isinstance(objs[i], (int, long, float, complex))
        if not b: return False
    return True

def _filter_strings( strArray, patterns, mode ):
    """
    """
    assert mode in ['and','or']
    assert len(patterns)>0,"_filter_strings: empty patterns: "+patterns+" mode"+mode
    matches = []
    for s in strArray:
        bAdd = None
        if mode == "and":
            bAdd = True
            for p in patterns:
                if bAdd and re.search( p, s, re.IGNORECASE) is None: bAdd = False
        if mode == "or":
            bAdd = False
            for p in patterns:
                if re.search( p, s, re.IGNORECASE) is not None: 
                    bAdd = True
                    continue
        if bAdd == True: matches.append( s )
    return matches  
    

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

# parallelization utils
def _parallel_for_loop( array, blocks_n, funct, params ):
    assert len(array)>0
    assert blocks_n>0
    assert blocks_n <= len(array)
    assert funct
    assert params
    psize = multiprocessing.cpu_count()
    assert psize > 0
    msg = "_parallel_for_loop objects="+str(len(array))+" processes="+str(blocks_n)+" cpus="+str(psize)
    sw = StopWatch(msg)
    log.info( msg )
    
    subarrays = _split_list(array,blocks_n)
    assert len(subarrays)==blocks_n
    
    pool = multiprocessing.Pool( processes=blocks_n )
    
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    
    # start all jobs
    for subarr in subarrays:
        assert len(subarr)>0
        pool.apply_async( funct, args = (subarr, queue, params, ) )
    
    pool.close()
    pool.join()
    
    # extract and return results
    log.debug("Extracting results from queue...")
    results = []
    while not queue.empty(): results.append(queue.get())
    #print "results",results
    assert len(results) == blocks_n, "results="+str(len(results))+" blocks_n="+str(blocks_n) #len(results) == blocks_n or 
    log.info( "_parallel_for_loop: end" )
    sw.tick("ended")
    return results

def _float_eq( a, b, err=1e-08):
    return abs(a - b) <= err
