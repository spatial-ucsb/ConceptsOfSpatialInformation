{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FunctionalDependencies #-}

-- the content concept of a field
-- core question: what is the value of an attribute at a position and an instant?
-- all fields are spatio-temporal, defined for a location and time
-- the positions can be georeferenced or not (allowing, for example, for non-georeferenced images)
-- field models can be raster or vector (then with an interpolation function)
-- (c) Werner Kuhn
-- latest change: Feb 6, 2016
-- TO DO
--	do a vector field model and find out how to abstract over raster and vector representations of the field function
-- 	generalize map algebra operations to a single operation on multiple fields, taking a function as input (TH idea), signature [value]->value?
-- 	look at the toolbox of QGIS whether it does all map algebra with one underlying operator! 
-- import qualified Data.Array.Repa as Repa (to implement fields with more computations, richer index types, and IO formats)

module Field where

import Location
import Time
import Theme
import Data.Array 

-- the class of all field types
-- fields have a field function as well as a location and a time over which they are defined
-- functional dependencies avoid type ambiguities (some of them at runtime!)
class (LOCATIONS location coord, TIMES time scale) => FIELDS field location coord time scale | field -> location coord, field -> time scale where
	domain :: field -> (location coord, time scale) -- the location and the time over which the field is defined
	valueAt :: field -> Position coord -> Instant scale -> Value -- needs to check if position and instant are within domain and period
{-	insideOf, outsideOf :: field -> object -> field -- cutting or masking the domain by an object
	during, except :: field -> time scale -> field -- cutting or masking the period
	local :: [field position value] -> ([value] -> value') -> field position value' object event
	focal :: field position value object event -> (neighborhood -> value') -> field position value' object event -- with a kernel function to compute the new values based on the values in the neighborhood of the position
	zonal :: field position value object event -> (zones -> value') -> field position value' object event -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions	
-}

-- a raster model of a 2d spatial field function 
type FieldFunction2d = Array (Int, Int) Value
a2 :: FieldFunction2d
a2 = array (p11t, p22t) [(p11t, Boolean True), (p21t, Boolean False), (p12t, Boolean True), (p22t,Boolean False)]

-- instantaneous 2d raster fields
data RasterField2d = RasterField2d FieldFunction2d (MBR Int) (Instant Int)
rf1 = RasterField2d a2 mbr1 i1 

instance FIELDS RasterField2d MBR Int Instant Int where
	domain (RasterField2d a m i) = (m, i)
	valueAt (RasterField2d a m i) p t 
		| not (positionIn p m) = error "position outside field domain"
		| not (contains i t) = error "instant outside field domain"
		| otherwise = a ! (pos2Tup2 p)

-- TESTS
ft1 = domain rf1
ft2 = valueAt rf1 p11 i1
