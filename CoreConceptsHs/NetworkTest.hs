module NetworkTest where

import Network
import NetworkImpl

myGraph :: CCGraph
myGraph = mkGraph [1, 2, 3, 2] [(1, 2, 2), (2, 3, 3), (3, 1, 2), (2, 3, 3)]

main :: IO ()
main = do
	print $ nodes myGraph
	print $ edges myGraph
	putStrLn ""
	print $ shortestPath myGraph 1 2
	print $ shortestPath myGraph 2 1
	print $ shortestPath (addEdge myGraph (2, 1, 6)) 2 1
