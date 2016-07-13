{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of field
-- core question: what is the value of an attribute at a position? (not at a location, as locations are aggregated positions)
-- positions (not locations) define the spatial (Worboys) or locational (Galton) framework
-- they need to fall within the field domain (defined by locations) to return values
-- field constructors can take a time parameter (constructing a snapshot field at that time)
-- continuity (of the field function, or of space, time, and value) is optional - as it is in Galton 2004
-- coverage simply means that the field function is total (but the domain can be a set of nodes, e.g., capital cities)
-- (c) Werner Kuhn
-- latest change: July 11, 2016

-- TO DO
-- make sure the field concept accomodates networks as domains (including embedded edges)
-- generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea)
-- look at the toolbox of QGIS whether it does all map algebra with one underlying operator! 
-- import qualified Data.Array.Repa as Repa (to implement fields with more computations, richer index types, and IO formats)
-- consider using https://hackage.haskell.org/package/grid-7.8.5/docs/Math-Geometry-Grid.html for tesselations

module Field where

import Location
import Data.Array 
import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

type TimeStamp = UTCTime
ts1 = (read "2016-07-01 19:16 UTC") :: TimeStamp -- an arbitrary time stamp

-- thematic values are taken from extended measurement scales
-- modeled as a sum type (until we need more)
-- admitting "object fields" (Cova) as fields with polygon values 
-- are there Haskell packages for measurement scales?
data Value = Boolean Bool | Nominal String | Ordinal String | Interval Integer | Ratio Float | TimeSeries [(TimeStamp, Value)] | Region Location deriving (Eq, Show)

-- the class of all field types
-- a field restricts the domain of a function (from Positions to Values) to a set of Locations
-- its granularity can be different from that of the domain (coarser as well as finer?)
class FIELDS field where
	valueAt :: field -> Position -> Value -- implementations need to check whether position is in domain
	domain :: field -> [Location] -- this allows multiple kinds of geometries!
	grain :: field -> Length 
{-	insideOf, outsideOf :: field -> extent -> field -- cutting or masking the domain by another extent
	local :: [field position value] -> ([value] -> value') -> field position value' extent
	focal :: field position value extent -> (neighborhood -> value') -> field position value' extent -- with a kernel function to compute the new values based on the values in the neighborhood of the position
	zonal :: field position value extent -> (zones -> value') -> field position value' extent -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions
-}

-- a raster model of a field function
type FieldArray2d = Array (Coord, Coord) Value

-- the simplest domain definition is a set of raster positions (MBR would be an alternative)
data RasterField2d = RasterField2d FieldArray2d [Position] TimeStamp

instance FIELDS RasterField2d where
	valueAt (RasterField2d a pList t) p = if positionIn p pList then a!(pos2pair p) else error "position outside field domain"
	domain (RasterField2d a pList t) = [pList]
	grain (RasterField2d a pList t) = 1 -- the index resolution of the array sets the granularity
	
-- a set of point observations
type FieldPoints = [(Position, Value)]

-- a mockup interpolation function (use IDW on numeric values https://www.e-education.psu.edu/geog486/node/1877)  
interpolate :: FieldPoints -> Position -> Value
interpolate fp p = snd (fp!!0)

-- vector fields
-- constructed from point observations, interpolation function, granularity, and time stamp
data VectorField = VectorField FieldPoints (FieldPoints -> Position -> Value) [Location] Length TimeStamp

instance FIELDS VectorField where
	valueAt (VectorField fp interpolate d g t) p = interpolate fp p -- should check if p in d
	domain (VectorField fp interpolate  d g t) = d
	grain (VectorField fp interpolate  d g t) = 1 -- this should be set in constructor

-- TESTS
a2 :: FieldArray2d
a2 = array (p11p, p22p) [(p11p, Boolean True), (p21p, Boolean False), (p12p, Boolean True), (p22p, Boolean False)]
rf = RasterField2d a2 pList ts1
fieldPoints :: FieldPoints
fieldPoints = [(p11, Boolean True), (p21, Boolean False), (p12, Boolean True), (p22, Boolean False)]
vf = VectorField fieldPoints interpolate [pList] 1 ts1
ft1 = valueAt rf p11
ft2 = valueAt vf p11
ft3 = domain rf
ft4 = domain vf
ft5 = grain rf
ft6 = grain vf
test = (ft1, ft2, ft3, ft4, ft5, ft6)

