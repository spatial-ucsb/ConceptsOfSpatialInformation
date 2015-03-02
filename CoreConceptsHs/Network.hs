{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}

-- core concept: network
-- core question: are two nodes connected? what is the shortest path between them?
-- all nodes are objects (until I see a need to change this)
-- how to bring in PATH and LINK from earlier specs?
-- (c) Werner Kuhn, Nov 23, 2014

module Network where

-- the class of all network types
-- both nodes and edges can be labeled
class NETWORK network node edge where
	nodes :: network -> [node]
	edges :: network -> [edge]
	addNode :: network -> node -> network
	addEdge :: network -> edge -> network -- link existing nodes
	degree :: network -> node -> Int -- number of edges to other nodes
	connected :: network -> node -> node -> Bool -- can the second node be reached from the first?
	shortestPath :: network -> node -> node -> [edge]
	distance :: network -> node -> node -> Int -- length of the shortest path as number of nodes
	breadthFirst :: network -> node -> Int -> [node]  -- all nodes at distance Int from a node

-- Graph representation in FGL
-- also, use FGL to determine core queries
