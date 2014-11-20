{-# LANGUAGE MultiParamTypeClasses #-} 
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}

-- core concept: network
-- core question: are two nodes connected? 
-- the nodes are always objects (until I see another need)
-- implementations may be best in FGL
-- use FGL to determine core queries
-- how to bring in PATHS and LINKS?
-- (c) Werner Kuhn, Oct 28, 2014

module Network where

import Object

-- the class of all network types
-- both nodes and edges can be labeled
class OBJECTS node => NETWORKS network node link where
	nodes :: network -> [node]
	edges :: network -> [edge]
	addNode :: network -> node -> network
	addEdge :: network -> edge -> network -- link existing nodes 
	linking :: network -> edge -> (node, node)
	degree :: network -> node -> Int -- number of edges to other nodes
	connected :: network -> node -> node -> Bool -- can the second node be reached from the first?
	shortestPath :: network -> node -> node -> [edge] 
	distance :: network -> node -> node -> Int -- length of the shortest path
	breadthFirst :: network -> node -> Int -> [node]  -- all nodes at distance Int from a node

-- Graph representation in FGL
