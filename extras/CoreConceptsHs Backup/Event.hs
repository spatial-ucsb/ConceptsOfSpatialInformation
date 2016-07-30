{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of an event
-- core questions: when did this event happen? what happened before? what participants does the event have?
-- events are instantiated process portions with fields, objects, and networks as participants
-- an event collection is an event (in analogy to a feature collection being a feature)
-- (c) Werner Kuhn
-- latest change: Feb 6, 2016
-- To Do
-- compute event outcomes: central, but how to specify? do simple examples

module Event where

import Time

-- the class of all event types
-- Eq captures identity
-- events are bounded in time, but do not need an explicit boundary
class Eq (event time) => EVENTS event time where
	bounds :: event time -> Interval time

data InstantEvent time = InstantEvent (Instant time) deriving (Eq, Show)

instance (Eq time, Ord time) => EVENTS InstantEvent time where
 	bounds (InstantEvent (Instant t1 trs1)) = Interval (Instant t1 trs1) (Instant t1 trs1)

-- TESTS
ie1, ie2 :: InstantEvent Int
ie1 = InstantEvent i1
ie2 = InstantEvent i2
et1 = bounds ie1