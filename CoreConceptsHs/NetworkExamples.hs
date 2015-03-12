module NetworkExamples where

import Network
import NetworkImpl
import Data.List
import Data.Graph.Inductive.Basic

myGraph :: CCGraph
myGraph = mkGraph [1, 2, 3, 2] [(1, 2, 2), (2, 3, 3), (3, 1, 2), (2, 3, 3)]

-- hardcoded graph from ../data/networks/karate.gml
karateGraph :: CCGraph
karateGraph = undir $ mkGraph [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34] [(2, 1, 1), (3, 1, 1), (3, 2, 1), (4, 1, 1), (4, 2, 1), (4, 3, 1), (5, 1, 1), (6, 1, 1), (7, 1, 1), (7, 5, 1), (7, 6, 1), (8, 1, 1), (8, 2, 1), (8, 3, 1), (8, 4, 1), (9, 1, 1), (9, 3, 1), (10, 3, 1), (11, 1, 1), (11, 5, 1), (11, 6, 1), (12, 1, 1), (13, 1, 1), (13, 4, 1), (14, 1, 1), (14, 2, 1), (14, 3, 1), (14, 4, 1), (17, 6, 1), (17, 7, 1), (18, 1, 1), (18, 2, 1), (20, 1, 1), (20, 2, 1), (22, 1, 1), (22, 2, 1), (26, 24, 1), (26, 25, 1), (28, 3, 1), (28, 24, 1), (28, 25, 1), (29, 3, 1), (30, 24, 1), (30, 27, 1), (31, 2, 1), (31, 9, 1), (32, 1, 1), (32, 25, 1), (32, 26, 1), (32, 29, 1), (33, 3, 1), (33, 9, 1), (33, 15, 1), (33, 16, 1), (33, 19, 1), (33, 21, 1), (33, 23, 1), (33, 24, 1), (33, 30, 1), (33, 31, 1), (33, 32, 1), (34, 9, 1), (34, 10, 1), (34, 14, 1), (34, 15, 1), (34, 16, 1), (34, 19, 1), (34, 20, 1), (34, 21, 1), (34, 23, 1), (34, 24, 1), (34, 27, 1), (34, 28, 1), (34, 29, 1), (34, 30, 1), (34, 31, 1), (34, 32, 1), (34, 33, 1)]

-- helper functions
oneZip :: a -> [b] -> [(a, b)]
oneZip a b = zip (replicate (length b) a) b

headZip :: [a] -> [(a, a)]
headZip a = oneZip (head a) $ tail a

combinations :: [a] -> [(a, a)]
combinations [] = []
combinations (x:xs) = oneZip x xs ++ combinations xs

-- examples
main :: IO ()
main = do
	putStrLn "Example for shortestPath with directed and effectively undirected graphs"
	putStrLn $ " nodes: " ++ (show $ nodes myGraph)
	putStrLn $ " edges: " ++ (show $ edges myGraph)
	putStrLn ""
	putStrLn $ " 1 -> 2 : " ++ (show $ shortestPath myGraph 1 2)
	putStrLn $ " 2 -> 1 : " ++ (show $ shortestPath myGraph 2 1)
	putStrLn $ " 2 -> 1 (after adding an edge from 2 to 1): " ++ (show $ shortestPath (addEdge myGraph (2, 1, 6)) 2 1)
	putStrLn ""
	putStrLn ""
	putStrLn ""
	putStrLn "Analysis of the network of friendships between the 34 members of a karate club at a US university, as described by Wayne Zachary in 1977."
	putStrLn ""
	putStr "People who don't maintain a friendship inside the karate club:\n "
	putStrLn $ if length lonely == 0 then "non" else show lonely
	putStrLn ""
	putStr "How many friendships are there?\n "
	putStrLn $ show $ (length $ edges karateGraph) `div` 2
	putStrLn ""
	putStr "And who maintains the highest number of friendships?\n "
	putStrLn $ show $ map (\node -> (node, delete node $ breadthFirst karateGraph node 1)) popular
	putStrLn ""
	putStr "We can look for a seperated group by checking if one member is connected to everybody else.\n "
	putStrLn $ if all (\edge -> connected karateGraph (fst edge) $ snd edge) $ headZip $ nodes karateGraph then "All the members are connected." else "There is a seperated group."
	putStrLn ""
	putStr "So as a friend of a friend of a friend and so on everyone is connected to everybody else. But what's the highest number of people needed to create a connection between two members?\n "
	putStrLn $ show $ (maximum $ map length allPaths) - 1
		where
			degrees :: [(Node, Int)]
			degrees = zip (nodes karateGraph) $ map (\node -> degree karateGraph node) $ nodes karateGraph
			selectLonely :: (Node, Int) -> Bool
			selectLonely (_, i) = i == 0
			selectPopular :: (Node, Int) -> Bool
			selectPopular (_, i) = i == (maximum $ map snd degrees :: Int)
			lonely :: [Node]
			lonely = map fst $ filter selectLonely degrees
			popular :: [Node]
			popular = map fst $ filter selectPopular degrees
			allPaths :: [[(Node, Node, Weight)]]
			allPaths = map (\pair -> shortestPath karateGraph (fst pair) $ snd pair) $ combinations $ nodes karateGraph
