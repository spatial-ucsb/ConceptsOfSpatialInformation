{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the base concept of location
-- spatial properties and relations 
-- vector geometry could be represented as well-known text (http://en.wikipedia.org/wiki/Well-known_text)
-- better alternative encoding would be GeoJSON (http://www.macwright.org/2015/03/23/geojson-second-bite.html)
-- (c) Werner Kuhn
-- latest change: February 6, 2016

module Location where

-- locations are values of spatial attributes 
-- unifying vector and raster representations
-- behavior is defined by spatial relations (add more as needed)
-- places are objects, not values, i.e. they do not belong here
class LOCATIONS location coord where
	positionIn :: Position coord -> location coord -> Bool
-- 	contains :: location coord -> location coord -> Bool
--	distance :: location coord -> location coord -> coord 

-- the number of dimensions
-- Int would be too general; it could be Nat, but that comes with no obvious choice of library
-- also, there are no computations on the number of dimensions
data Dimension = D1 | D2 | D3 deriving (Eq, Ord, Show) 
errorDim = "different dimensions"

-- spatial reference systems
-- for now just an enumeration 
-- possibly use http://en.wikipedia.org/wiki/SRID later
data SRS = WGS84 | Local deriving (Eq, Show)
errorSRS = "different spatial reference systems"

-- positions in any space 
-- controlling for dimension
-- turns out similar to http://hackage.haskell.org/package/hgeometry 
data Position coord = Position [coord] Dimension SRS deriving (Eq, Show)

instance LOCATIONS Position Int where 
	positionIn (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = clist1 == clist2
{-	contains (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = clist1 == clist2
	distance (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = sum (map abs (zipWith (-) clist2 clist1)) -- in discrete spaces, use manhattan metric
-}

{- euclidean, for Floating coord
-- float coords will need a more sophisticated Eq implementation (with tolerance, or Id based)
	distance (Position clist1 dim1 srs1) (Position clist2 dim2 srs2) = 	
	let sqr a = a*a 
	in if (srid1==srid2 && d1==d2) then sqrt (sum (map sqr (zipWith (-) c2 c1))) else error "different spaces"
-}

-- bounding boxes
-- parameterization does NOT guarantee same coord type in both positions!
data MBR coord = MBR (Position coord) (Position coord) deriving (Eq, Show)

instance LOCATIONS MBR Int where 
	positionIn (Position clist1 dim1 srs1) (MBR (Position clist2 dim2 srs2) (Position clist3 dim3 srs3))
		| (dim1 /= dim2) || (dim2 /= dim3) = error errorDim
		| (srs1 /= srs2) || (srs2 /= srs3) = error errorSRS
		| otherwise = error "not yet implemented"
{-	contains (MBR (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)) (MBR (Position clist3 dim3 srs3) (Position clist4 dim4 srs4))
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = error "not yet implemented"
	distance (MBR (Position clist1 dim1 srs1) (Position clist2 dim2 srs2)) (MBR (Position clist3 dim3 srs3) (Position clist4 dim4 srs4))
		| dim1 /= dim2 = error errorDim
		| srs1 /= srs2 = error errorSRS
		| otherwise = sum (map abs (zipWith (-) clist2 clist1)) -- in discrete spaces, use manhattan metric
-}
-- converting positions to tuples (only 2-tuples for now)
-- needed as array indices (in Field), but may be useful otherwise
-- SRID intentionally dropped, can be added if needed
pos2Tup2 :: Position coord -> (coord, coord) 
pos2Tup2 (Position c D2 s) = (c!!0,c!!1)

-- TESTS
p11, p12, p21, p22 :: Position Int 
p11 = Position [1, 1] D2 Local
p12 = Position [1, 2] D2 Local
p21 = Position [2, 1] D2 Local
p22 = Position [2, 2] D2 Local

p11t = pos2Tup2 p11
p12t = pos2Tup2 p12
p21t = pos2Tup2 p21
p22t = pos2Tup2 p22

p3, p4 :: Position Float 
p3 = Position [1.0, 2.0] D2 Local
p4 = Position [2.0, 1.0] D2 Local

mbr1 :: MBR Int
mbr1 = MBR p11 p22
mbr2 :: MBR Float
mbr2 = MBR p3 p4

--lt1 = show (distance p11 p22)
--lt2 = show (distance p3 p4)
