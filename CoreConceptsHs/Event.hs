{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: event 
-- core questions: when did this event happen? what properties and relations does the event have? what participants does it have?
-- events are process portions with fields, objects, and networks as participants
-- conjecture: all events can be seen as movements at some granularity
-- properties and relations are thematic only
-- temporal properties and relations get defined here, as they only apply to events
-- spatial properties and relations of events come from their participants 
-- positioning and bounding of events themselves does not seem appropriate
-- computing event outcomes: central, but how to specify? do simple examples
-- (c) Werner Kuhn
-- latest change: Nov 23, 2014

module Event where

import Location
import Object

-- the class of all event types
-- Eq captures identity
-- all participants are objects for now
class (Eq event, OBJECT object) => EVENT event object where
	when :: event -> Date -- timing the event
	within :: event -> Period -- containing the event
	during :: event -> event -> Bool 
	before :: event -> event -> Bool 
	after :: event -> event -> Bool 
	overlap :: event -> event -> Bool
	-- complete with Allen relations

-- Times
type Date = Int -- time point, as 19950204 or 199502 or 1995, following the ISO standard
type Period = (Date, Date) -- time interval
