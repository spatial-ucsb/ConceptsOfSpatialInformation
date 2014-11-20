{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: event 
-- core questions: when did this happen? what properties and relations does the event have? what participants does it have?
-- events are process portions with participants: fields, objects, networks
-- conjecture: all events are movements at some granularity
-- properties and relations are limited to thematic ones (same as for objects)
-- temporal properties and relations defined here, as they only apply to events
-- the spatial properties and relations of events come from their participants (objects, for now)
-- also, spatial properties and relations come from making events a sub-class of objects (there is no reason not to, as they have all object behavior)
-- computing event outcomes: central, but how to specify? do simple examples
-- (c) Werner Kuhn
-- latest change: Nov 20, 2014

module Event where

import Location
import Object

-- the class of all event types
-- Eq captures identity
-- all events are objects!
-- all participants are objects for now
class (Eq event, OBJECTS event, OBJECTS object, LOCATE event object) => EVENTS event object where
	within :: event -> Maybe Period -- any time interval containing the event
	when :: event -> Maybe Period -- any time interval timing the event
	during :: event -> event -> Bool 
	before :: event -> event -> Bool 
	after :: event -> event -> Bool 
	overlap :: event -> event -> Bool
	-- complete with Allen relations

-- Times
type Date = Int -- time point, as 19950204 or 199502 or 1995, following the ISO standard
type Period = (Date, Date) -- time interval
