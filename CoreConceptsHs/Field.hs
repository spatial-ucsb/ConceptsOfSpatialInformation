{-# LANGUAGE MultiParamTypeClasses #-}

-- the content concept of field
-- core question: what is the value of an attribute at a position?
-- extents define the spatial (Worboys) or locational (Galton) framework
-- positions need to fall within extents to return values
-- field constructors take a time parameter (constructing a snapshot field at that time)
-- continuity (of the field function, or of space, time, and value) is optional - as it is in Galton 2004
-- coverage simply means that the function is total (but the extent can be a set of nodes, e.g., capital cities)
-- admit "object fields": they are really just fields with more complex values (but not literally objects)
-- (c) Werner Kuhn
-- latest change: July 1, 2016

-- TO DO
-- make sure the field concept accomodates fields on networks and time series at multiple positions
-- generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea)
-- look at the toolbox of QGIS whether it does all map algebra with one underlying operator! 
-- import qualified Data.Array.Repa as Repa (to implement fields with more computations, richer index types, and IO formats)

module Field where

import Location
import Data.Array 
import System.Time -- ClockTime and CalendarTime; see RealWorld Haskell "Dates and Times"; do we need this or is Data.Time replacing it? 
import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

-- thematic values, taken from measurement scales
-- modeled as a sum type (until we need more)
-- any generic behavior across scales? probably just equality (by definition)
-- are there Haskell packages for measurement scales?
-- add time series of values, to return as whole values
data Value = Boolean Bool | Nominal String | Ordinal String | Interval Int | Ratio Float deriving (Eq, Show)

-- the class of all field types
-- fields restrict a function (Positions to Values) to an extent (as the domain)
class FIELDS field where
	valueAt :: field -> Position -> Value -- needs to check if position is within domain
	-- domain returning extent
{-	insideOf, outsideOf :: field -> extent -> field -- cutting or masking the domain by an extent
	local :: [field position value] -> ([value] -> value') -> field position value' extent
	focal :: field position value extent -> (neighborhood -> value') -> field position value' extent -- with a kernel function to compute the new values based on the values in the neighborhood of the position
	zonal :: field position value extent -> (zones -> value') -> field position value' extent -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions
-}

-- a raster model of a 2d field 
-- with a raster function
type FieldArray2d = Array (Coord, Coord) Value
a2 :: FieldArray2d
a2 = array (p11t, p22t) [(p11t, Boolean True), (p21t, Boolean False), (p12t, Boolean True), (p22t, Boolean False)]

data RasterField2d = RasterField2d FieldArray2d MBR UTCTime
timeStamp = (read "2016-07-01 19:16 UTC") :: UTCTime -- arbitrary time
rf = RasterField2d a2 mbr timeStamp

instance FIELDS RasterField2d where
	valueAt (RasterField2d a mbr t) p = if positionIn p mbr then a!(pos2Tup2 p) else error "position outside field domain"

-- a vector model of a field
-- with a point set and an interpolation function
type FieldPoints = [(Position, Value)]
fieldPoints :: FieldPoints
fieldPoints = [(p11, Boolean True), (p21, Boolean False), (p12, Boolean True), (p22, Boolean False)]

-- a mockup interpolation function
-- eventually use IDW on numeric values https://www.e-education.psu.edu/geog486/node/1877 
interpolate :: FieldPoints -> Position -> Value
interpolate fp p = snd (fp!!0)

data VectorField = VectorField FieldPoints (FieldPoints -> Position -> Value)
vf = VectorField fieldPoints interpolate

instance FIELDS VectorField where
	valueAt (VectorField fp interpolate) p = interpolate fp p

-- TESTS
ft1 = valueAt rf p11
ft2 = valueAt vf p11
