{-# LANGUAGE MultiParamTypeClasses #-}

-- the content concept of a field
-- core question: what is the value of an attribute at a position?
-- the spatio-temporal framework (in the sense of Worboys) is taken here to be an object (having temporal state)
-- (c) Werner Kuhn
-- latest change: Mar 8, 2016

-- TO DO
--	do a vector field model and find out how to abstract over raster and vector representations of the field function
-- 	make sure the field concept accomodates fields on networks and time series at multiple positions
-- 	generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea)
-- 	look at the toolbox of QGIS whether it does all map algebra with one underlying operator! 
--	import qualified Data.Array.Repa as Repa (to implement fields with more computations, richer index types, and IO formats)

module Field where

import Location
import Time
import Theme
import Object
import Data.Array 

-- the class of all field types
-- fields restrict a function (Positions to Values) to an object (as the domain)
class FIELDS field where
	valueAt :: field -> Position -> Value -- needs to check if position is within domain
{-	insideOf, outsideOf :: field -> object -> field -- cutting or masking the domain by an object
	local :: [field position value] -> ([value] -> value') -> field position value' object event
	focal :: field position value object event -> (neighborhood -> value') -> field position value' object event -- with a kernel function to compute the new values based on the values in the neighborhood of the position
	zonal :: field position value object event -> (zones -> value') -> field position value' object event -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions
-}

-- a raster model of a 2d field 
-- with a raster function
type FieldArray2d = Array (Coord, Coord) Value
a2 :: FieldArray2d
a2 = array (p11t, p22t) [(p11t, Boolean True), (p21t, Boolean False), (p12t, Boolean True), (p22t, Boolean False)]

data RasterField2d = RasterField2d FieldArray2d (Box MBR)
rf = RasterField2d a2 box

instance FIELDS RasterField2d where
	valueAt (RasterField2d a (Box mbr)) p = if positionIn p mbr then a!(pos2Tup2 p) else error "position outside field domain"

-- a vector model of a field
-- with a point set and an interpolation function
type FieldPoints = [(Position, Value)]
fieldPoints :: FieldPoints
fieldPoints = [(p11, Boolean True), (p21, Boolean False), (p12, Boolean True), (p22, Boolean False)]

-- a mockup interpolation
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
