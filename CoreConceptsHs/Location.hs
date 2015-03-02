{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
-- core concept: location
-- defining spatial relations and properties
-- core questions: where is this? is this in relation r to that? what is in relation r to this?
-- location questions get asked about instances of the other core concepts (fields, objects, networks, events)
-- these instances are always taken at the time (i.e. in a state) at which they play the figure and ground roles
-- the answer to the question "is Santa Barbara in the United States" is different for "the United States now" and "the United States before 1848"
-- thus, figures and grounds are spatio-temporal, but the locating relations are not!
-- space and time need to be separated, not treated as 4d, in order to deal with examples like the Santa Barbara one
-- positions are purely spatial
-- move to partWhole class, which is not always locating, isPart :: figure -> ground -> Bool
-- (c) Werner Kuhn
-- latest change: November 22, 2014

module Location where

-- the class of all locating relations
class LOCATED figure ground where
	isAt :: figure -> ground -> Bool
	isIn :: figure -> ground -> Bool
	-- add more spatial relations as needed

-- the class of all positioned entities
-- putting the point constraint into the method avoids a second type parameter
class POSITIONED figure where
	position :: POINT point => figure -> point -- a point positioning the figure

-- the class of all bounded entities
-- putting the extent constraint into the method avoids a second type parameter
class BOUNDED figure where
	bounds :: EXTENT shape => figure -> shape -- an extent bounding the figure

-- the class of all geometries
-- all geometries need coordinate reference systems, but making it explicit creates too much overhead
class GEOMETRY geometry -- where what?

-- the class of all points (non-extended geometries)
class GEOMETRY geometry => POINT geometry -- where distance?

-- the class of all extended geometries
class GEOMETRY geometry => EXTENT geometry where
	box :: (P2, P2) -> geometry

-- geometries more complex than a point are represented as well-known text (http://en.wikipedia.org/wiki/Well-known_text)
type Coordinate = Int

type P2 = (Coordinate, Coordinate) -- we need tuples to be able to use them as array indices; repa may take lists?

instance GEOMETRY P2

instance POINT P2

instance GEOMETRY (P2,P2)
instance EXTENT (P2,P2) where
	box (p1, p2) = (p1, p2)


type SRID = Int -- the spatial reference system id (EPSG code, see http://en.wikipedia.org/wiki/SRID)



{-distance :: Coordinates -> Coordinates -> Int
distance [a1, o1] [a2, o2] = abs (a2 - a1) + abs (o2 - o1) -- Manhattan distance, assuming projected coordinates in m
walkingDistance = 1000.0-}
-- need procedure calls to WKT operations anywhere

{-p, q :: Coord2
p =  (0,0)
q =  (2,2)
pq = [p..q]-}

--pq = [p..q]

{-instance Ix Position where
	range (p,q) = [p..q]
	index (p,q) p =
	inRange :: (a,a) -> a -> Bool
	rangeSize :: (a,a) -> Int-}

{-
type Geometry = String -- well-known text representation
instance GEOMETRY Geometry
geomFromP2 :: P2 -> Geometry
geomFromP2 (x,y) = "POINT (" ++ show x ++ space ++ show y ++ ")"

geomFrom2P2 :: (P2,P2) -> Geometry
geomFrom2P2 ((x1,y1),(x2,y2)) = "MULTIPOINT (" ++ show x1 ++ " " ++ show y1 ++ comma ++ space ++ show x2 ++ space ++ show y2 ++ ")"

space = " "
comma = ","
-}
