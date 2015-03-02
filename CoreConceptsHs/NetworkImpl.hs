{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}

module NetworkImpl where

import Network
import Data.List
import Data.Maybe
import Data.Graph.Inductive.Graph
import Data.Graph.Inductive.PatriciaTree
import Data.Graph.Inductive.Query.BFS

type CCNode = String
type CCEdge = String
type CCGraph = Gr CCNode CCEdge

labNode :: (Eq node, Eq edge) => (Gr node edge) -> Node -> LNode node
labNode graph node = fromJust $ find select $ labNodes graph
	where
		select :: LNode node -> Bool
		select (n, _) = n == node

labEdge :: (Eq node, Eq edge) => (Gr node edge) -> Edge -> LEdge edge
labEdge graph (a, b) = fromJust $ find select $ labEdges graph
	where
		select :: LEdge edge -> Bool
		select (n1, n2, _) = n1 == a && n2 == b

instance NETWORK CCGraph (LNode CCNode) (LEdge CCEdge) where
	nodes = labNodes
	edges = labEdges
	addNode network node = insNode node network
	addEdge network edge = insEdge edge network
	degree network node = deg network (fst node)
	connected network a b = 0 /= length (shortestPath network a b :: [LEdge CCEdge])
	shortestPath network a b = map label edges
		where
			label :: Edge -> LEdge CCEdge
			label edge = labEdge network edge
			edges :: [Edge]
			edges = zip path $ tail path
			path :: [Node]
			path = esp (fst a) (fst b) network
	distance network a b = length (shortestPath network a b :: [LEdge CCEdge])
	breadthFirst network node distance = map (label . fst) $ filter select $ level (fst node) network
		where
			label :: Node -> LNode CCNode
			label node = labNode network node
			select :: (Node, Int) -> Bool
			select (_, d) = d <= distance

emptyCCGraph :: CCGraph
emptyCCGraph = empty
