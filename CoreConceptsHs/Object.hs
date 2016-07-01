{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of an object
-- core questions: where is this object? is it the same as that object?
-- collections of objects are objects too (consistent with feature collections being features in OGC)
-- objects have temporal state (manifested in their spatial and thematic properties and relations)
-- (c) Werner Kuhn
-- latest change: Mar 7, 2016

-- TO DO
-- think of boundedness by upper hierarchy level of a tesselation (AURIN does that?)

module Object where

import Location

-- the class of all object types
-- parameterized in the underlying extent type
-- Eq captures identity (each object type has its own identity criterion) 
-- all objects are bounded (expressed by mbr), but they may not have a boundary 
-- object properties and relations are to be defined on concrete object types, as none of them are generic
class (EXTENTS extent, Eq (object extent)) => OBJECTS object extent where
	bounds :: object extent -> MBR

-- object IDs (for types that use one)
newtype Id = Id Int deriving (Eq, Show)

-- points of interest 
data POI extent = POI Id extent deriving Show
instance Eq (POI Position) where 
	POI i p == POI j q = i == j
instance OBJECTS POI Position where
	bounds (POI i p) = MBR p (coords p)

-- box objects
data Box extent = Box extent deriving Show
instance Eq (Box MBR) where 
	Box mbr1 == Box mbr2 = mbr1 == mbr2
instance OBJECTS Box MBR where
	bounds (Box mbr) = mbr

-- tests
poi1, poi2 :: POI Position
poi1 = POI (Id 1) p11
poi2 = POI (Id 2) p22
ot1 = bounds poi1

box :: Box MBR
box = Box mbr
