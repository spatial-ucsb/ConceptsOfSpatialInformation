{-# LANGUAGE MultiParamTypeClasses #-} 
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeOperators #-} -- to allow for new index types for Repa arrays (not sure)

-- core concept: field
-- core question: what is the value of an attribute at a position? 
-- other core operations: set value, local, focal, zonal operations
-- should there be a resampling op?
-- positions can include time and are always discrete
-- implementations in Array (http://www.haskell.org/tutorial/arrays.html) or Repa (http://www.haskell.org/haskellwiki/Numeric_Haskell%3a_A_Repa_Tutorial)?
-- instances will come from solar energy project
-- partitioned fields should probably be a derived class
-- (c) Werner Kuhn, Aug 11, 2014

module Field where

import Location
import Data.Array 
--import qualified Data.Array.Repa as Repa -- to represent fields with more computations, richer index types, and many io formats

-- the class of all field types
class FIELDS field position value where
	getValue :: field position value -> position -> value   
	setValue :: field position value -> position -> value -> field position value
	domain :: field position value -> Geometry -- Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries
	neighborhood :: field position value -> position -> Geometry -- the neighborhood of a position, described by its boundary or a set of positions
	zone :: field position value -> position -> Geometry -- the zone of a partitioned field containing a position, described by its boundary or a set of positions
	local :: field position value -> (value -> value') -> field position value' -- map algebra's local operations, with a function to compute the new values
	focal :: field position value -> (position -> value') -> field position value' -- map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
	zonal :: field position value -> (position -> value') -> field position value' -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions


-- Array representation
a2 :: Array P2 String
a2 = array ((1,1),(2,2)) [((1,1),"ul"), ((1,2),"ur"), ((2,1),"ll"), ((2,2),"lr")]

instance FIELDS Array P2 String where
	getValue a p = a!p
	setValue a p v = a // [(p, v)]
	domain a = geomFrom2P2 (bounds a)
	local a f = fmap f a -- arrays are instances of the functor class
--	focal a k = needs a better field