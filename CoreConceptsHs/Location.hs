{-# LANGUAGE MultiParamTypeClasses #-}

-- the base concept of location
-- spatial properties and relations for all other core concepts
-- including spatial reference systems
-- spaces can be vector, raster, or network
-- all entities are modeled as single types (at most as sum types)
-- type classes are possible (with type dependencies), but not (yet) needed
-- (c) Werner Kuhn
-- latest change: August 15, 2016

-- TO DO
-- import a geometry library: http://hackage.haskell.org/package/hgeometry ?
-- define bounding boxes by a position and coordinate shifts (2 positions would be ambiguous on the sphere)
-- vector geometry could be represented as well-known text: http://en.wikipedia.org/wiki/Well-known_text 
-- better encoding would be GeoJSON http://www.macwright.org/2015/03/23/geojson-second-bite.html 
-- use a 3-valued (check Kleene) or a fuzzy logic for positionIn


module Location where

import Data.List -- for set membership (elem) 

type Length = Integer -- one-dimensional size measure

-- coordinates are distances from hyperplanes, measured by counts of units (i.e., they have granularity)
-- used for vector, raster, and (embedded) network models
-- only used for space, not for time or space-time
-- all implementations are discrete, while conceptualizations can be continuous
-- Haskell Integers have arbitrarily fine precision, so no need for any other coordinate types!
type Coord = Length
type CoordList = [Coord]

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

-- positions are point-like locations in any space
-- called "locations" in Galton 2004, but "position" agrees better with ordinary and technical use
-- implemented as lists of coordinates, with reference system and dimension
data Position = Position CoordList Dimension SRS deriving (Eq, Show)
dim (Position clist dim srs) = dim
srs (Position clist dim srs) = srs
coords (Position clist dim srs) = clist
coord (Position clist dim srs) dimension 
	| dim < dimension = error "dimension out of range"
	| otherwise = clist!!dimension 

-- distance
distance :: Position -> Position -> Length 
distance p1 p2 = error "not yet implemented" -- could easily do manhattan

-- converting positions to coordinate pairs 
-- spatial reference system dropped
pos2pair :: Position -> (Coord, Coord) 
pos2pair (Position c 2 s) = (c!!0,c!!1)

-- locations are extents (spatial footprints) in any dimension, including Positions and (parts of) networks
-- they are bounded, with or without a boundary
-- they can have multiple unconnected parts 
-- currently implemented as a Position (setting the reference system and dimension) plus a list of coordinate lists 
-- this implementation needs to be refined, based on actual footprints (is a position list best, with srs from head?)
-- behavior is defined by spatial relations, such as positionIn (add more as needed)
data Location = Location Position [CoordList] deriving (Eq, Show) -- the position sets the dimension and reference system 
positionIn :: Position -> Location -> Bool
positionIn pos (Location p cs) = (pos == p) || (elem (coords pos) cs)
boundary :: Location -> Maybe Location
boundary location = Just location -- dummy implementation!


-- TESTS
p11 = Position [1,1] 2 Local
p12 = Position [1,2] 2 Local
p21 = Position [2,1] 2 Local
p22 = Position [2,2] 2 Local

p11p = pos2pair p11
p12p = pos2pair p12
p21p = pos2pair p21
p22p = pos2pair p22

loc = Location p11 [coords p12, coords p21, coords p22]

lt1 = positionIn p11 loc
lt2 = positionIn p22 loc


