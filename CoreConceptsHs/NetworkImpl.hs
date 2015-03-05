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

type Weight = Int
type CCGraph = Gr () Weight

instance NETWORK CCGraph Node (LEdge Weight) where
	nodes = map fst . labNodes
	edges = labEdges
	addNode graph node = insNode (node, ()) graph
	addEdge = flip $ insEdge
	degree = deg
	connected graph a b = 0 /= distance graph a b
	shortestPath graph a b = map label edges
		where
			label :: Edge -> (LEdge Weight)
			label (a, b) = (a, b, 1)
			edges :: [Edge]
			edges = zip path $ tail path
			path :: [Node]
			path = esp a b graph
	distance graph a b = length (shortestPath graph a b)
	breadthFirst graph node distance = map fst $ filter select $ level node graph
		where
			select :: (Node, Int) -> Bool
			select (_, d) = d <= distance

mkGraph :: [Node] -> [LEdge Weight] -> CCGraph
mkGraph nodes ledges = Data.Graph.Inductive.Graph.mkGraph (map label nodes) ledges
	where
		label :: Node -> LNode ()
		label node = (node, ())
