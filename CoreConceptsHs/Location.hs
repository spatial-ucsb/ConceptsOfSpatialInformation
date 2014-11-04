{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: location 
-- a generic spatial relation
-- core questions: where is this? is this in relation r to that? what is in relation r to this?
-- such questions concern instances of the other core spatial concepts (fields, objects, networks, events) or their parts
-- these instances are always taken at some time (i.e. in a state) to play figure and ground roles
-- the answer to "is Santa Barbara in the United States" is different for "the United States now" and "the United States before 1848"
-- thus, figures and grounds are spatio-temporal, but not the locating relations!
-- space and time need to be separated, not treated as 4d, to deal with examples like the Santa Barbara one
-- positions are better kept purely spatial
-- (c) Werner Kuhn
-- latest change: August 2nd, 2014

module Location where

-- the class of all locating relations
class LOCATE figure ground where
	isAt :: figure -> ground -> Bool 
	isIn :: figure -> ground -> Bool 
	isPart :: figure -> ground -> Bool 
	-- add any spatial relations
	-- no isNear yet, as it is not deterministic (maybe define an isNearerThan?)

-- Geometries 
type Coordinate = Int
type P2 = (Coordinate, Coordinate) -- we need tuples to be able to use them as array indices; repa may make lists possible?
type P3 = (Coordinate, Coordinate, Coordinate)
type Geometry = String -- well-known text representation of geometries: http://en.wikipedia.org/wiki/Well-known_text

space = " "
comma = ","

geomFromP2 :: P2 -> Geometry
geomFromP2 (x,y) = "POINT (" ++ show x ++ space ++ show y ++ ")"

geomFrom2P2 :: (P2,P2) -> Geometry
geomFrom2P2 ((x1,y1),(x2,y2)) = "MULTIPOINT (" ++ show x1 ++ " " ++ show y1 ++ comma ++ space ++ show x2 ++ space ++ show y2 ++ ")"

type Date = Int -- time point, as 19950204 or 199502 or 1995, following the ISO standard
type Duration = (Date, Date) -- time interval

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
	range (p,q) = [p..q]	index (p,q) p = 	inRange :: (a,a) -> a -> Bool	rangeSize :: (a,a) -> Int-}
	