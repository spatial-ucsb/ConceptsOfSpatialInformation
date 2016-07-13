{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of an object
-- core questions: where is this object? is it the same as that object?
-- collections of objects are objects too (consistent with feature collections being features in OGC)
-- objects have temporal state (manifested in their spatial and thematic properties and relations)
-- (c) Werner Kuhn
-- latest change: July 13, 2016

-- TO DO
-- consider boundedness by upper hierarchy level of a tesselation (AURIN does that?)

module Object where

import Location

-- the class of all object types
-- Eq captures identity (each object type has its own identity criterion) 
-- all objects are bounded, but they may not have a boundary 
-- object properties and relations to be defined on concrete object types (none are generic)
class Eq object => OBJECTS object where
	bounds :: object -> Location -- need to differentiate object geometry from object boundary

-- object IDs (for types that use one)
newtype Id = Id Int deriving (Eq, Show)

-- points of interest 
data POI = POI Id Position deriving Show
instance Eq POI where 
	POI i p == POI j q = i == j
instance OBJECTS POI where
	bounds (POI i p) = [p]

-- tests
poi1, poi2 :: POI
poi1 = POI (Id 1) p11
poi2 = POI (Id 2) p22
ot1 = bounds poi1
