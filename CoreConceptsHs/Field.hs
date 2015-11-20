{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeOperators #-} -- to allow for new index types for Repa arrays (not sure)

-- core concept: field
-- core question: what is the value of an attribute at a position?
-- other core operations: neighborhood, map algebra, change domain
-- currently, only the local operation takes multiple fields as inputs
-- fields are bounded, with the bounds defining their domain
-- fields have state in time, but positions are purely spatial
-- (c) Werner Kuhn
-- latest change: Nov 20, 2015

module Field where

import Location
import Data.Array
--import qualified Data.Array.Repa as Repa -- to represent fields with more computations, richer index types, and many io formats

-- the class of all field types
class (POINT position, BOUNDED (field position value)) => FIELD field position value where
	valueAt :: field position value -> position -> value
	neighborhood :: field position value -> position -> [position]
	zones :: field position value -> [(value -> bool)] -> [[position]] -- do we need to make sure the subsets partition the domain? is this the best form of a partitioning function?
	local :: [field position value] -> ([value] -> value') -> field position value' 
	focal :: field position value -> (neighborhood -> value') -> field position value' -- with a kernel function to compute the new values based on the values in the neighborhood of the position
	zonal :: field position value -> (zones -> value') -> field position value' -- map algebra's zonal operations, with a function to compute the new values based on zones containing the positions

-- Haskell implementations of fields can be done in Array (http://www.haskell.org/tutorial/arrays.html) or Repa (http://www.haskell.org/haskellwiki/Numeric_Haskell%3a_A_Repa_Tutorial)
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
