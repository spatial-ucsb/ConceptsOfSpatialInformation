{-# LANGUAGE MultiParamTypeClasses #-}

-- the base concept of time
-- temporal properties and relations  
-- (c) Werner Kuhn
-- latest change: February 5, 2016
-- TO DO
-- check OGC terminology for time
-- what about cyclic time?

module Time where

-- times are values of temporal attributes (temporal analogues to locations, not to metric geometries)
-- they are parameterized in their time scale, which has to be at least ordinal (e.g., geological eras)  
-- their behavior is captured by Allen's relations (add more of them as needed)
class Ord scale => TIMES time scale where
	instantIn :: Instant scale -> time scale -> Bool
	precedes :: time scale -> time scale -> Bool 
 	contains :: time scale -> time scale -> Bool
	separation :: Num scale => time scale -> time scale -> scale -- a distance on the time scale (not an interval)

-- temporal reference systems
-- based on https://github.com/52North/PostTIME/wiki/List-of-available-reference-systems 
data TRS = CAL Int | TCS Int | ORD Int  deriving (Eq, Show)
errorTRS = "different temporal reference systems"

-- instants
data Instant scale = Instant scale TRS deriving (Eq, Show)

instance TIMES Instant Int where
 	instantIn (Instant t1 trs1) (Instant t2 trs2) = if (trs1==trs2) then (t1==t2) else error errorTRS
 	contains (Instant t1 trs1) (Instant t2 trs2) = if (trs1==trs2) then (t1==t2) else error errorTRS
	precedes (Instant t1 trs1) (Instant t2 trs2) = if (trs1==trs2) then (t1<t2) else error errorTRS
	separation (Instant t1 trs1) (Instant t2 trs2) = if (trs1==trs2) then (t2-t1) else error errorTRS

-- intervals
data Interval scale = Interval (Instant scale) (Instant scale) deriving (Eq, Show)

instance TIMES Interval Int where
 	instantIn (Instant t1 trs1) (Interval (Instant t2 trs2) (Instant t3 trs3))
 		= if (trs1==trs2 && trs2==trs3) then (t2<=t1 && t1<=t3) else error errorTRS
	precedes (Interval (Instant t1 trs1) (Instant t2 trs2)) (Interval (Instant t3 trs3) (Instant t4 trs4))
 		= if (trs1==trs2 && trs2==trs3 && trs3==trs4) then (t2<=t3) else error errorTRS
 	contains (Interval (Instant t1 trs1) (Instant t2 trs2)) (Interval (Instant t3 trs3) (Instant t4 trs4))
 		= if (trs1==trs2 && trs2==trs3 && trs3==trs4) then (t1<=t3 && t4<=t2) else error errorTRS
	separation (Interval (Instant t1 trs1) (Instant t2 trs2)) (Interval (Instant t3 trs3) (Instant t4 trs4)) 
		= if (trs1==trs2 && trs2==trs3 && trs3==trs4) then (t3-21) else error errorTRS

-- TESTS
i1, i2, i3, i4 :: Instant Int
i1 = Instant 1 (CAL 1)
i2 = Instant 2 (CAL 1)
i3 = Instant 3 (CAL 1)
i4 = Instant 4 (CAL 1)

iv1, iv2 :: Interval Int
iv1 = Interval i1 i2
iv2 = Interval i3 i4
iv3 = Interval i1 i4
iv4 = Interval i2 i3