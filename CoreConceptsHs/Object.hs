{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: object 
-- core questions: where is this object? what are its properties and relations? is it the same as that object?
-- properties and relations are limited to thematic ones
<<<<<<< HEAD
-- all spatial properties and relations come from Location (only for other objects as grounds, so far)
-- objects have no temporal properties or relations
-- objects have state, queried through their spatial and thematic properties and relations
-- (c) Werner Kuhn
-- latest change: Nov 21, 2014
=======
-- spatial properties and relations come from Location
-- objects have no temporal properties or relations
-- can we have something that corresponds to OGC's get capabilities, returning implemented properties and relations?
-- (c) Werner Kuhn
-- latest change: Nov 20, 2014
>>>>>>> FETCH_HEAD

module Object where

import Location

-- the class of all object types
-- Eq captures identity
<<<<<<< HEAD
class (Eq object, LOCATED object object, POSITIONED object, BOUNDED object) => OBJECT object where
=======
-- LOCATE captures spatial relations between objects (others may yet need to be instantiated)
class (Eq object, LOCATE object object) => OBJECTS object where
>>>>>>> FETCH_HEAD
	get :: (object -> value) -> object -> value
	set :: (object -> value) -> object -> value -> object
	is :: (object -> object -> Bool) -> object -> object -> Bool
<<<<<<< HEAD
=======
	be :: (object -> object -> Bool) -> (object -> object) -> object -- needs testing and a decision on how to record relations in objects
>>>>>>> FETCH_HEAD
	get property = property
	is relation = relation
