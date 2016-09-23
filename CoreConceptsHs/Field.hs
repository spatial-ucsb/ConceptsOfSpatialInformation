{-# LANGUAGE MultiParamTypeClasses #-}

-- the content concept of field
-- core question: what is the value of an attribute at a position? 
-- positions define the spatial (Worboys) or locational (Galton) framework
-- they need to fall within the field's domain (defined by a location) to return values
-- the domain can be any location (e.g., also just a set of located nodes)
-- field constructors can take a time parameter (constructing a snapshot field at that time)
-- continuity (of the field function, or of space, time, or value) is optional - as it is in Galton 2004
-- tesselations are a subclass of fields (not an alternative where zones instead of positions have values!)
-- (c) Werner Kuhn
-- latest change: September 21, 2016

-- TO DO
-- generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea)
-- consider using https://hackage.haskell.org/package/grid-7.8.5/docs/Math-Geometry-Grid.html for tesselations
-- are there Haskell packages for measurement scales?

module Field where

import Location
import Data.Array 
import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

type TimeStamp = UTCTime
ts1 = (read "2016-07-01 19:16 UTC") :: TimeStamp -- an arbitrary time stamp

-- thematic values are taken from (extended) measurement scales
-- modeled as a sum type (until we need more)
-- admitting "object fields" (Cova) in the sense of fields with extents as values 
-- also admitting value vectors and time series
data Value = Boolean Bool | Nominal String | Ordinal String | Interval Integer | Ratio Float | Region Location | Vector [Value] | TimeSeries [(TimeStamp, Value)] deriving (Eq, Show)

-- the class of all field types
-- a field restricts the domain of a function (from Positions to Values) to a Location
-- the field's granularity can be different from that of the domain (coarser as well as finer?)
-- how do we admit multiple kinds of geometries (raster, vector) in the domain?
-- the class seems to have all OGC Coverages as valid models (check)
class FIELDS field where
	valueAt :: field -> Position -> Value -- implementations need to check whether position is in domain
	domain :: field -> Location -- this allows multiple kinds of geometries!
	newDomain :: field -> Location -> field -- Location replaces the old domain
	grain :: field -> Length 
	local :: field -> (Value -> Value) -> field 
--	focal :: field -> (Extent -> Value) -> field -- with a kernel function to compute the new values based on the values in the neighborhood of the position
--	zonal :: field -> ([Extent] -> Value) -> field  -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions
{- Worboys on zonal operations:
"A zonal operation results in the following kind of derivation of a new field. For each location x:1. Find the zone Zi in which x is contained.2. Compute the values of the field function f applied to each point in Zi.3. Derive a single value of the new field from the values computed in step 2, possibly taking special account of the value of the field at x.For example, given a layer of temperatures and a zoning into administrative regions, a zonal operation is required to create a layer of average temperatures for each region."
Thus, zonal is a constructor for tesselations!
-}


-- tesselations are fields with a partition into a set of zones
class FIELDS field => TESSELATION field --where

-- a raster model of a field function
type FieldArray2d = Array (Coord, Coord) Value

data RasterField2d = RasterField2d FieldArray2d Location TimeStamp

instance FIELDS RasterField2d where
	valueAt (RasterField2d a loc t) p = if positionIn p loc then a!(pos2pair p) else error "position outside field domain"
	domain (RasterField2d a loc t) = loc
	grain (RasterField2d a loc t) = 1 -- the index resolution of the array sets the granularity
	
-- a set of point observations
type FieldPoints = [(Position, Value)]

-- a mockup interpolation function (use IDW on numeric values https://www.e-education.psu.edu/geog486/node/1877)  
interpolate :: FieldPoints -> Position -> Value
interpolate fp p = snd (fp!!0)

-- vector fields
-- constructed from point observations, interpolation function, granularity, and time stamp
data VectorField = VectorField FieldPoints (FieldPoints -> Position -> Value) Location Length TimeStamp

instance FIELDS VectorField where
	valueAt (VectorField fp interpolate d g t) p = interpolate fp p -- should check if p in d
	domain (VectorField fp interpolate  d g t) = d
	grain (VectorField fp interpolate  d g t) = 1 -- this should be set in constructor

-- TESTS
a2 :: FieldArray2d
a2 = array (p11p, p22p) [(p11p, Boolean True), (p21p, Boolean False), (p12p, Boolean True), (p22p, Boolean False)]
rf = RasterField2d a2 loc ts1
fieldPoints :: FieldPoints
fieldPoints = [(p11, Boolean True), (p21, Boolean False), (p12, Boolean True), (p22, Boolean False)]
vf = VectorField fieldPoints interpolate loc 1 ts1
ft1 = valueAt rf p11
ft2 = valueAt vf p11
ft3 = domain rf
ft4 = domain vf
ft5 = grain rf
ft6 = grain vf
test = (ft1, ft2, ft3, ft4, ft5, ft6)

