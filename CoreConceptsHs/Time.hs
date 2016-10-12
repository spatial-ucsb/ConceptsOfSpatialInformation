-- basic time values and operations for core concepts
-- (c) Werner Kuhn
-- latest change: October 7, 2016

-- TO DO

module Time where

import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

type Instant = UTCTime
ts = (read "2016-07-01 19:16 UTC") :: Instant -- an arbitrary time stamp

type Duration = DiffTime

type Period = (Instant, Instant)

instantIn :: Instant -> Period -> Bool
instantIn i p = (fst p) <= i && (snd p) >= i
