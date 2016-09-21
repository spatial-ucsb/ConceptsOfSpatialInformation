{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE FunctionalDependencies #-}

-- the content concept of a network
-- core question: are two nodes connected? what is the shortest path between them?
-- how to bring in PATH and LINK from earlier specs?
-- (c) Werner Kuhn
-- latest change: Feb 27, 2016
-- additions Wei Luo, based on ....

-- TO DO
-- make networks a subclass of objects
-- Graph representation in FGL
-- also, use FGL to determine core queries


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

--add by Wei
-- network level
	isDirected:: network -> Bool --- is a directed network or not. 
    isSimple:: network -> Bool --does not have loops (self-edges) and does not have multiple identical edges	
	isTree: network -> Bool -- contain no circuits; N nodes and N-1 edges.
	--averageDegree :: network ->float --the average degree of a network (needs use case, is not core)
	isClique :: network -> Bool --- is a completely connected simple graph (check terminology)
	isStronglyConnected:: network ->Bool ---has a path from each node to every other node and vice versa (check definition)
	--isweaklyconnecteddirected:: network ->Bool ---it is connected if we disregard the edge directions.
	graphDiameter :: network -> Int --- the maximum distance between any pair of nodes in the graph
	--averagePathLength :: network -> float -- Average path length/distance for a connected graph
	graphEfficiency :: network -> float -- average inverse distance To avoid infinities in graphs that are not connected and digraphs that are not strongly connected (check definition)
    weighted:: network -> Bool -- edges with weights (need to figure out how to handle weights)
-- node's centrality    
    inDegree :: network -> node -> Int -- number of head ends adjacent to a node
	outDegree :: network -> node -> Int -- number of tail ends adjacent to a node
    betweenness :: network -> node -> float -- the number of shortest paths from all nodes to all others that pass through that node (why float?)
	closeness :: network -> node -> float -- a measure of the degree to which an individual is near all other individuals in a network (check definition) 
	eigenvector :: network -> node -> float --assigns relative scores to all nodes in the network based on the concept that connections to high-scoring nodes contribute more to the score of the node in question than equal connections to low-scoring nodes.
	--?Katz centrality :: network ->node -> float -- the number of all nodes that can be connected through a path, while the contributions of distant nodes are penalized. 
	clustering coefficient :: network -> node -> float --a measure of the degree to which nodes in a graph tend to cluster together (check definition)
-- edge
    isLoop:: network -> node -> node -> Bool -- Multiple edges between two nodes
	--isloop:: network -> node -> Bool -- a vertex with itself
    adjacent:: network -> node -> node -> Bool -- there is an edge joining two nodes
	--isCircuit:  network -> node1 -> node ->....->node1 -> Bool --a path that starts and ends at the same nodes
    --isCycle: network -> node1 -> node ->....->node1 -> Bool --a circuit that does not revisit any nodes
	isBridge: network -> edge -> Bool --if we erase the edge, the graph becomes disconnected
	
	