module NetworkTest where

import Network
import NetworkImpl
import Data.Graph.Inductive.Graph

main :: IO ()
main = putStrLn $ prettify $ addEdge (addNode (addNode emptyCCGraph (1, "Node1")) (2, "Node2")) (1, 2, "Edge1-2")
