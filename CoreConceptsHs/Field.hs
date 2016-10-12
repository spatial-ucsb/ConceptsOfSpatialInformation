{-# LANGUAGE MultiParamTypeClasses #-}

-- the content concept of field
-- core question: what is the value of an attribute at a position? 
-- positions define the spatial (Worboys) or locational (Galton) framework
-- positions outside the field's domain have the null value (making the function complete)
-- in our non-fourdimensionalist theory, positions are not in space-time but only in space
-- time dependence is either homogeneous across the domain, producing a stack of time stamped fields, or local, producing time series as values
-- continuity (of the field function, or of space, time, or value) is optional - as it is in Galton 2004
-- tesselations are partitioned fields 
-- (c) Werner Kuhn
-- latest change: October 12, 2016

-- TO DO
-- generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea)
-- for non-square regular rasters use https://hackage.haskell.org/package/grid-7.8.5/docs/Math-Geometry-Grid.html
-- define zonal operation such that it produces tessselation
{-"A zonal operation results in the following kind of derivation of a new field. For each location x:1. Find the zone Zi in which x is contained.2. Compute the values of the field function f applied to each point in Zi.3. Derive a single value of the new field from the values computed in step 2, possibly taking special account of the value of the field at x.For example, given a layer of temperatures and a zoning into administrative regions, a zonal operation is required to create a layer of average temperatures for each region."
-}

module Field where

import Location
import Time  
import Data.Array 

-- values are taken from (extended) measurement scales
-- modeled as a sum type (until we need different operators on them)
-- admitting "object fields" (Cova) in the sense of fields with extents as values 
-- also admitting value vectors and time series
-- are there Haskell packages for measurement scales? do we need one?
data Value = Null | Boolean Bool | Nominal String | Ordinal String | Interval Integer | Ratio Float | Region Extent | Vector [Value] | TimeSeries [(Instant, Value)] deriving (Eq, Show)

-- the class of all field types
-- a field restricts the domain of a function (from Positions to Values) to an extent 
-- the field's granularity can be different from that of the domain (coarser as well as finer?)
-- the class seems to have all OGC Coverages as valid models (check!)
class FIELDS field where
	valueAt :: field -> Position -> Value -- check whether position and instant are in domain!
	domain :: field -> Config 
	setDomain :: field -> Config -> field
	grain :: field -> Length
	local :: field -> ([Value] -> Value) -> field 
--	focal :: field -> (Extent -> Value) -> field -- with a kernel function to compute the new values based on the values in the neighborhood of the position
--	zonal :: field -> ([Extent] -> Value) -> field  -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions

-- tesselations are fields partitioned into a set of zones
class FIELDS field => TESSELATION field --where

-- a raster model of a spatial field function
type FieldArray2d = Array (Coord, Coord) Value
data RasterField2d = RasterField2d FieldArray2d Config Instant

instance FIELDS RasterField2d where
	valueAt (RasterField2d a d t) pos = a!(pos2pair pos) -- check what arrays return for positions outside (but need to check for positionIn domain!)
	domain (RasterField2d a d t) = d
	grain (RasterField2d a d t) = 1 -- the array index resolution defines the granularity (but should be in the world)

{-	
-- a set of point observations
type FieldPoints = [(Position, Value)]

-- a mockup interpolation function (use IDW on numeric values https://www.e-education.psu.edu/geog486/node/1877)  
interpolate :: FieldPoints -> Position -> Value
interpolate fp p = snd (fp!!0)

-- vector fields
-- constructed from point observations, interpolation function, extent, instant, and spatial granularity
data VectorField = VectorField FieldPoints (FieldPoints -> Position -> Value) Domain Length

instance FIELDS VectorField where
	valueAt (VectorField fp interpolate e i l) p = interpolate fp p -- should check if p in d
	domain (VectorField fp interpolate  e i l) = e
	grain (VectorField fp interpolate  e i l) = 1 -- this should be set in constructor

-- TESTS
a2 :: FieldArray2d
a2 = array (p11p, p22p) [(p11p, Boolean True), (p21p, Boolean False), (p12p, Boolean True), (p22p, Boolean False)]
--rf = RasterField2d a2 loc ts
fieldPoints :: FieldPoints
fieldPoints = [(p11, Boolean True), (p21, Boolean False), (p12, Boolean True), (p22, Boolean False)]
--vf = VectorField fieldPoints interpolate loc 1 ts
ft1 = valueAt rf p11
ft2 = valueAt vf p11
ft3 = domain rf
ft4 = domain vf
ft5 = grain rf
ft6 = grain vf
test = (ft1, ft2, ft3, ft4, ft5, ft6)
--}
