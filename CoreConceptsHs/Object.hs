{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: object 
-- core questions: what are this object's properties and relations? 
-- examples: boundary (property) and location (relation)
-- can we have something that corresponds to OGC's get capabilities, returning defined properties and relations?
-- (c) Werner Kuhn
-- latest change: Jul 25, 2014


module Object where

import Location

-- the class of all object types
-- Eq captures identity
class Eq object => OBJECTS object where
	bounds :: object -> Geometry -- boundedness, returning any geometry containing the object
	get :: (object -> value) -> object -> value
	is :: (object -> object -> Bool) -> object -> object -> Bool
	get property o = property o
	is relation o1 o2 = relation o1 o2
