{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}

-- the base concept of location
-- spatial entities, properties, and relations for content concepts
-- including spatial reference systems
-- spaces can be vector, raster, or network
-- using the term "location" as a spatial value (not object!)
-- all entities modeled as single types (at most sum type)
-- type classes are possible (with type dependencies), but not yet needed
-- (c) Werner Kuhn
-- latest change: July 13, 2016

-- TO DO
-- define bounding boxes by a position and coordinate shifts (2 positions would be ambiguous on the sphere)
-- import a geometry library: http://hackage.haskell.org/package/hgeometry ?
-- vector geometry could be represented as well-known text: http://en.wikipedia.org/wiki/Well-known_text 
-- better encoding would be GeoJSON http://www.macwright.org/2015/03/23/geojson-second-bite.html 
-- use a 3-valued (check Kleene) or a fuzzy logic for positionIn


module Location where

import Data.List -- for set membership

type Length = Integer -- one-dimensional size measure

-- coordinates are distances from hyperplanes, measured by counts of units (i.e., they have granularity)
-- used for vector, raster, and (embedded) network models
-- only used for space, not for time or space-time
-- all implementations are discrete, while conceptualizations can be continuous
-- Haskell Integers have arbitrarily fine precision, so no need for any other coordinate types!
type Coord = Length

-- the number of spatial dimensions
-- Int is too general, but simplifies dimension tests
type Dimension = Int 
errorDim = "dimension error"

-- spatial reference systems
-- for now just an enumeration 
-- possibly use http://en.wikipedia.org/wiki/SRID 
-- fixes the spatial unit (i.e., what length does a Coord unit correspond to?), WKT UNIT
data SRS = WGS84 | Local deriving (Eq, Show)
errorSRS = "spatial reference system error"

-- positions are "point-like" locations in any space
-- called "locations" in Galton 2004, but position agrees better with ordinary use
-- implemented as lists of coordinates, with reference system and dimension
data Position = Position [Coord] Dimension SRS deriving (Eq, Show)
dim (Position clist dim srs) = dim
srs (Position clist dim srs) = srs
coords (Position clist dim srs) = clist
coord (Position clist dim srs) dimension 
	| dim < dimension = error "dimension out of range"
	| otherwise = clist!!dimension 

type PosList = [Position] -- too liberal (allowing for mixing dimensions as well as srs)

-- distance
distance :: Position -> Position -> Length 
distance p1 p2 = error "not yet implemented" -- could easily do manhattan

-- converting positions to coordinate pairs 
-- spatial reference system dropped, can be added if needed (need it in array!)
pos2pair :: Position -> (Coord, Coord) 
pos2pair (Position c 2 s) = (c!!0,c!!1)

-- locations are extents (regions) in any dimension 
-- including Positions
-- bounded, with or without a boundary
-- unifying vector, raster, and graph geometries
-- currently implemented as lists of positions (which gives them a reference system and dimension)
-- their behavior is defined by spatial relations, such as positionIn (add more as needed)
-- should dimensions and reference systems be constrained for these relations?
type Location = PosList -- singleton allows Positions as Locations
positionIn :: Position -> Location -> Bool
positionIn pos loc = elem pos loc
boundary :: Location -> Maybe Location
boundary location = Just [head location] -- dummy implementation!


-- TESTS
p11 = Position [1,1] 2 Local
p12 = Position [1,2] 2 Local
p21 = Position [2,1] 2 Local
p22 = Position [2,2] 2 Local

p11p = pos2pair p11
p12p = pos2pair p12
p21p = pos2pair p21
p22p = pos2pair p22

pList = [p11, p12, p21, p22]

lt1 = positionIn p11 pList
lt2 = positionIn p22 pList


