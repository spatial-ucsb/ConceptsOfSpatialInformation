{-# LANGUAGE MultiParamTypeClasses #-}

-- the base concept of location
-- spatial entities, properties, and relations for instances of content concepts
-- using the term "location" for the relation, "extent" for the noun (where it is a value, not an object)
-- spaces can be vector, raster, or network
-- (c) Werner Kuhn
-- latest change: July 1, 2016

-- TO DO
-- import a geometry library: http://hackage.haskell.org/package/hgeometry ?

module Location where

-- coordinates are distances from hyperplanes, as unit counts
-- covering vector, raster, and embedded network nodes
-- all implementations are necessarily discrete
-- conceptualizations can be continuous, if desired
-- Haskell Integers can have arbitrary fine precision
-- thus, no need for any other coordinate type!
type Coord = Integer
	
-- the number of spatial dimensions
-- Int is too general, but simplifies dimension tests
type Dimension = Int 
errorDim = "different dimensions"

-- spatial reference systems
-- for now just an enumeration 
-- possibly use http://en.wikipedia.org/wiki/SRID later
data SRS = WGS84 | Local deriving (Eq, Show)
errorSRS = "different spatial reference systems"

-- positions are lists of coordinates, controlled for dimension and given a reference system
-- called "locations" in Galton 2004, but position agrees better with ordinary use
data Position = Position [Coord] Dimension SRS deriving (Eq, Show)
dim (Position clist dim srs) = dim
srs (Position clist dim srs) = srs
coords (Position clist dim srs) = clist
coord (Position clist dim srs) dimension 
	| dim < dimension = error "insufficient dimensions"
	| otherwise = clist!!dimension 

-- distance
-- should they be discrete as well?
distance :: Position -> Position -> Double 
distance p1 p2 = error "not yet implemented"

-- converting positions to tuples 
-- so far, only 2-tuples needed (for field arrays) 
-- SRS intentionally dropped, can be added if needed
pos2Tup2 :: Position -> (Coord, Coord) 
pos2Tup2 (Position c 2 s) = (c!!0,c!!1)

-- extents are sub-spaces (regions) in any dimension
-- unifying vector, raster, and graph geometries
-- they may have boundaries
-- their behavior is defined by spatial relations (add more as needed)
-- primarily: positionIn, as set membership of positions in extents
-- vector geometry could be represented as well-known text (http://en.wikipedia.org/wiki/Well-known_text)
-- better encoding would be GeoJSON (http://www.macwright.org/2015/03/23/geojson-second-bite.html)
-- TO DO: go to 3-valued logic for positionIn
class EXTENTS extent where
	positionIn :: Position -> extent -> Bool
--	boundary :: extent coord -> Maybe MultiPoly -- needs a geometry package to implement

instance EXTENTS Position where 
	positionIn (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = clist1 == clist2

-- bounding boxes 
-- defined by a position and coordinate shifts
-- this may be the least ambiguous definition (2 positions is ambiguous on the sphere)
data MBR = MBR Position [Coord] deriving (Eq, Show)

instance EXTENTS MBR where 
	positionIn (Position clist1 dim1 srs1) (MBR (Position clist2 dim2 srs2) clist3)
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = foldr1 (&&) (zipWith3 between clist1 clist2 clist3) 
			where between c1 c2 c3 = (c2 <= c1) && c1 <= (c2+c3) 

-- TESTS
p11 = Position [1,1] 2 Local
p12 = Position [1,2] 2 Local
p21 = Position [2,1] 2 Local
p22 = Position [2,2] 2 Local

p11t = pos2Tup2 p11
p12t = pos2Tup2 p12
p21t = pos2Tup2 p21
p22t = pos2Tup2 p22

mbr = MBR p11 [1,1]

lt1 = positionIn p11 mbr
lt2 = positionIn p22 mbr


