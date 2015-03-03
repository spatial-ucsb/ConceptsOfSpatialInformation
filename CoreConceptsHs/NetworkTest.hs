module NetworkTest where

import Network
import NetworkImpl

myGraph :: CCGraph
myGraph = mkGraph [(1, "Node_1"), (2, "Node_2"), (3, "Node_3")] [(1, 2, "Edge_1_2"), (2, 3, "Edge_2_3"), (3, 1, "Edge_3_1")]

main :: IO ()
main = do
	print $ nodes myGraph
	print $ edges myGraph
	putStrLn ""
	print $ shortestPath myGraph (1, "") (2, "")
	print $ shortestPath myGraph (2, "") (1, "")
	print $ shortestPath (addEdge myGraph (2, 1, "Edge_2_1")) (2, "") (1, "")
