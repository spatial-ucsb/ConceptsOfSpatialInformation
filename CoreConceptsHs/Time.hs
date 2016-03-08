{-# LANGUAGE MultiParamTypeClasses #-}

-- the base concept of time
-- temporal properties and relations  
-- need to deal with: instants (done: UTCTime), intervals (as complex values, not entities), durations (as measurements), ...
-- distinguishing instants from intervals is important (cognitively, and if all instants are also intervals, infinite regression may result)
-- periods are events, not time values, i.e. they do not belong here
-- no class of time types, as there was no general and implementable behavior beyond Eq and Ord (and these are already available from types)
-- only specify what is required in content types!

-- (c) Werner Kuhn
-- latest change: February 15, 2016

-- TO DO
-- add more time types (or libraries) with well-defined reference systems
-- sync all modeling decisions with location
-- check OGC terminology for time
-- temporal reference systems (if needed): https://github.com/52North/PostTIME/wiki/List-of-available-reference-systems   
-- what about cyclic time?

module Time where

import System.Time -- ClockTime and CalendarTime; see RealWorld Haskell "Dates and Times"; do we need this or is Data.Time replacing it? 
import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

