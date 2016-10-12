{-# LANGUAGE MultiParamTypeClasses #-}

-- the base concept of location
-- defining spatial properties and relations 
-- including spatial reference systems
-- spaces can have vector, raster, or network geometries
-- all entities are modeled as single types (at most as sum types), no classes
-- (c) Werner Kuhn; latest change: October 7, 2016

-- TO DO
-- import a geometry library: http://hackage.haskell.org/package/hgeometry ?
-- vector geometry could be represented as well-known text: http://en.wikipedia.org/wiki/Well-known_text 
-- better encoding would be GeoJSON http://www.macwright.org/2015/03/23/geojson-second-bite.html 
-- define bounding boxes by a position and coordinate shifts (2 positions would be ambiguous on the sphere)
-- use a 3-valued (check Kleene) or a fuzzy logic for positionIn

module Location where

import Data.List -- for set membership (elem) 

type Length = Integer -- one-dimensional spatial size measure

-- coordinates are distances from hyperplanes, measured by counts of units (i.e., they have granularity)
-- used for vector, raster, and (embedded) network models
-- only used for space, not for time or space-time
-- all implementations are discrete, while conceptualizations can be continuous (with caution!)
-- Haskell Integers have arbitrarily fine precision, so there is no need for any other coordinate types!
type Coord = Length

-- the number of spatial dimensions
-- Int is too general, but simplifies dimension tests
type Dimension = Int 
errorDim = "dimension error"

-- spatial reference systems
-- for now just an enumeration; later possibly use http://en.wikipedia.org/wiki/SRID 
-- fixes the spatial unit (i.e., what length does a Coord unit correspond to?), WKT UNIT
data SRS = WGS84 | UTM | Local deriving (Eq, Show)
errorSRS = "spatial reference system error"

-- positions are minimal extents in vector or raster space: points or cells
-- called "locations" in Galton 2004, but "position" agrees better with ordinary and technical use
data Position = Position [Coord] Dimension SRS deriving (Eq, Show)
dim (Position clist dim srs) = dim
srs (Position clist dim srs) = srs
coords (Position clist dim srs) = clist
coord (Position clist dim srs) dimension 
	| dim < dimension = error "dimension out of range"
	| otherwise = clist!!dimension 

-- distance
distance :: Position -> Position -> Length 
distance p1 p2 = error "not yet implemented" -- could do manhattan, but wait for geometry package

-- converting positions to coordinate pairs (only needed as long as we use regular arrays)
-- spatial reference system dropped
pos2pair :: Position -> (Coord, Coord) 
pos2pair (Position c 2 s) = (c!!0,c!!1)

-- extents are simply connected spatial footprints in any dimension (including positions)
-- their behavior is defined by spatial relations, such as positionIn (add more as needed)
type Extent = [Position] -- the head of the list defines the SRS 
positionIn :: Position -> Extent -> Bool
positionIn pos ext = elem pos ext -- dummy implementation, just checking boundary points
boundary :: Extent -> Maybe Extent 
boundary extent = Just extent -- dummy implementation!

-- cheeses (for lack of a better term) are extents with holes
type Cheese = [Extent] -- head is exterior, tail is interiors

-- configurations are sets of cheeses
type Config = [Cheese] 

-- TESTS
p11 = Position [1,1] 2 Local
p12 = Position [1,2] 2 Local
p21 = Position [2,1] 2 Local
p22 = Position [2,2] 2 Local

p11p = pos2pair p11
p12p = pos2pair p12
p21p = pos2pair p21
p22p = pos2pair p22

ext = [p11, p12, p21, p22]

lt1 = positionIn p11 ext
lt2 = positionIn p22 ext


