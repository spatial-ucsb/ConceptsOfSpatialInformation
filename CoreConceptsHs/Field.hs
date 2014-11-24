{-# LANGUAGE MultiParamTypeClasses #-} 
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeOperators #-} -- to allow for new index types for Repa arrays (not sure)

-- core concept: field
<<<<<<< HEAD
-- core question: what is the value of an attribute at a point? 
-- other core operations: compute new fields from local, focal, and zonal operations
-- fields are bounded, the bounds defining their domain
-- fields have state in time, but points are purely spatial
-- (c) Werner Kuhn, Nov 23, 2014
=======
-- core question: what is the value of an attribute at a position? (get value) 
-- other core operations: set value, local, focal, zonal operations
-- positions can include time
-- Haskell implementations in Array (http://www.haskell.org/tutorial/arrays.html) or Repa (http://www.haskell.org/haskellwiki/Numeric_Haskell%3a_A_Repa_Tutorial)
-- instances from solar energy project
-- partitioned fields should probably be a derived class
-- deleted neighborhood observer, as it needs to be set, not observed
-- need to add neighborhood parameter to focal 
-- no need to change zonal parameters to include a zone definition (?)
-- (c) Werner Kuhn, Nov 17, 2014
>>>>>>> FETCH_HEAD

module Field where

import Location
import Data.Array 
--import qualified Data.Array.Repa as Repa -- to represent fields with more computations, richer index types, and many io formats

-- the class of all field types
<<<<<<< HEAD
class (POINT position, BOUNDED (field position value)) => FIELD field position value where
	getValue :: field position value -> position -> value   
=======
class LOCATE field => FIELDS field position value where
	getValue :: field position value -> position -> value   
	setValue :: field position value -> position -> value -> field position value
	domain :: field position value -> Geometry -- Domains can be described by corner points, convex hulls or boundaries
	zone :: field position value -> position -> Geometry -- the zone of a partitioned field containing a position, described by its boundary or a set of positions
>>>>>>> FETCH_HEAD
	local :: field position value -> (value -> value') -> field position value' -- map algebra's local operations, with a function to compute the new values
	focal :: field position value -> (position -> value') -> field position value' -- map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
	zonal :: field position value -> (position -> value') -> field position value' -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions

-- Haskell implementations in Array (http://www.haskell.org/tutorial/arrays.html) or Repa (http://www.haskell.org/haskellwiki/Numeric_Haskell%3a_A_Repa_Tutorial)

-- Array representation
a2 :: Array P2 String
a2 = array ((1,1),(2,2)) [((1,1),"ul"), ((1,2),"ur"), ((2,1),"ll"), ((2,2),"lr")]

instance BOUNDED (Array P2 String) where 
	bounds a = box (Data.Array.bounds a)

instance FIELD Array P2 String where
	getValue a p = a!p
	local a f = fmap f a -- arrays are instances of the functor class
--	focal a k = needs a better field

-- instances from solar energy project

