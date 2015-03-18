{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE FunctionalDependencies #-}

-- core concept: network
-- core question: are two nodes connected? what is the shortest path between them?
-- how to bring in PATH and LINK from earlier specs?
-- (c) Werner Kuhn, Michel Zimmer
-- latest change: Mar 2, 2015

module Network where

-- the class of all network types
-- both nodes and edges can be labeled
class NETWORK network node edge | network -> node, network -> edge where
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
