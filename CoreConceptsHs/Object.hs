{-# LANGUAGE MultiParamTypeClasses #-} 
-- core concept: object 
-- core questions: where is this object? what are its properties and relations? is it the same as that object?
-- properties and relations are limited to thematic ones
-- all spatial properties and relations come from Location (only for other objects as grounds, so far)
-- objects have no temporal properties or relations
-- objects have state, queried through their spatial and thematic properties and relations
-- (c) Werner Kuhn
-- latest change: Nov 21, 2014

module Object where

import Location

-- the class of all object types
-- Eq captures identity
class (Eq object, LOCATED object object, POSITIONED object, BOUNDED object) => OBJECT object where
	get :: (object -> value) -> object -> value
	is :: (object -> object -> Bool) -> object -> object -> Bool
	get property = property
	is relation = relation
