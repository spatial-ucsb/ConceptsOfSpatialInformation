{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of an object
-- core questions: where is this object? is it the same as that object?
-- collections of objects are objects too (consistent with feature collections being features in OGC)
-- objects have state, queried through their spatial and thematic properties and relations
-- (c) Werner Kuhn
-- latest change: Feb 6, 2016

module Object where

import Location

-- the class of all object types
-- Eq captures identity; each object type has its own identity criterion (which iD can use to generate an Id if needed)
-- all objects are bounded (though they may not have a boundary, nor a centroid or any other geometry!)
-- is mbr a good model? it is a bounding box, after all 
-- all other properties and relations to be defined on concrete object types (none of them are generic)
class Eq (object coord) => OBJECTS object coord where
	mbr :: object coord -> MBR coord

-- object IDs (for types that need one)
newtype Id = Id Int deriving (Eq, Show)

-- points of interest 
data POI coord = Poi Id (Position coord) deriving Show
instance Eq (POI coord) where 
	Poi i p == Poi j q = i == j
instance OBJECTS POI coord where
	mbr (Poi i p) = MBR p p

-- box objects
data Box coord = Box (MBR coord) deriving Show
instance Eq coord => Eq (Box coord) where 
	Box mbr1 == Box mbr2 = mbr1 == mbr2
instance Eq coord => OBJECTS Box coord where
	mbr (Box mbr) = mbr

-- tests
poi1 = Poi (Id 1) p11
poi2 = Poi (Id 2) p22
ot1 = mbr poi1
box1 = Box mbr1
box2 = Box mbr2