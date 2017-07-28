"""
These components implement the core concept 'network as defined in coreconcepts.py
:author: Fenja Kollasch, 06/2017
"""

from coreconcepts import CcNetwork
from objects import AstroObject
import copy
import sys


class AstroEdge(object):

    def __init__(self, goal, **attr):
        self.goal = goal
        self.attr = attr

    def __getattr__(self, item):
        if item in self.attr:
            return self.attr[item]
        else:
            raise AttributeError("No such attribute: {0}".format(item))

    def get(self, attr):
        return self.__getattr__(attr)


class Path(object):

    def __init__(self):
        self.nodes = []
        self.length = 0

    def add(self, node, length):
        self.nodes.append(node)
        self.length += length

    def __iter__(self):
        return self.nodes.__iter__()

    def __str__(self):
        s = "[Path: "
        for n in self.nodes:
            s = s + str(n) + " "
        s = s + "Length: {0}]".format(self.length)
        return s

    def __copy__(self):
        cpy = Path()
        cpy.nodes = self.nodes.copy()
        cpy.length = self.length
        return cpy


class AstroNetwork(AstroObject, CcNetwork):
    """
    Model networks as directional graph
    """

    def __init__(self, identity, **attr):
        """
        A network as an object, but also a graph of objects
        Does that make sense?
        :param identity: The identity of this network
        :param attr: Additional information
        """
        self.graph = dict()
        super(AstroNetwork, self).__init__(identity, **attr)

    def nodes(self):
        return self.graph.keys()

    def edges(self):
        edges = []
        for node in self.graph:
            edges.extend(self.graph[node])
        return edges

    def addNode(self, n, **attr):
        if isinstance(n, AstroObject):
            node = n
        else:
            node = AstroObject(n, **attr)
        self.graph[node] = []
        try:
            self.bounds().members.append(node)
        except AttributeError:
            pass

    def addNodes(self, nodes):
        for n in nodes:
            self.addNode(n)

    def addEdge(self, u, v, **attr):
        if u in self.graph and v in self.graph:
            self.graph[u].append(AstroEdge(v, **attr))
        else:
            raise NetworkError("Both nodes must be in the graph")

    def connected(self, u, v, visited=[]):
        if u in self.graph and v in self.graph:
            visited = visited + [u]
            found = False
            for edge in self.graph[u]:
                if edge.goal in visited:
                    found = False
                elif edge.goal == v:
                    found = True
                else:
                    found = False or self.connected(edge.goal, v, visited)
            return found
        return False

    def shortestPath(self, source, target, path=Path(), weight=None, color=None):
        """
        Finds the shortest path in the network
        :param source: Starting node
        :param target: goal node
        :param path: Currently taken path
        :param weight: The attribute that counts as weight
        Must be a tuple of weight attribute name and value
        :param color: Only nodes with this quality will be used
        must be a tuple of color attribute name and value
        :return: 
        """

        if source not in self.graph or target not in self.graph:
            raise NetworkError("Both nodes must be in the graph")

        if weight:
            path.add(source, weight[1])
        else:
            path.add(source, 1)
        if source.id == target.id:
            return path

        if source is None:
            return None

        shortest = None
        for edge in self.graph[source]:
            e_path = None
            try:
                if edge.goal not in path and (not color or edge.get(color[0]) == color[1]):
                    if weight:
                        e_path = self.shortestPath(edge.goal, target, copy.deepcopy(path),
                                                       (weight[0], edge.get(weight[0])), color)
                    else:
                        e_path = self.shortestPath(edge.goal, target, copy.deepcopy(path), color=color)
            except AttributeError:
                pass
            if e_path and (not shortest or e_path.length < path.length):
                shortest = e_path
        return shortest

    def nearest_node(self, obj):
        """
        Finds the nearest node to the given object
        Only works if the object and the nodes have a location
        :param obj: An object with a location
        :return: The nearest node to this position
        """
        nearest = None
        distance = None
        for node in self.graph.keys():
            d = obj.relation(node, 'distance')
            if not distance or d <= distance:
                distance = d
                nearest = node
        return nearest

    def degree(self, n):
        return len(self.graph[n])

    def distance(self, source, target, weight=None):
        if weight:
            return self.shortestPath(source, target, weight=(weight, 0)).length
        else:
            return self.shortestPath(source, target).length

    def breadthFirst(self, node, distance, nodes=[]):
        if node not in self.graph:
            raise NetworkError("Node must be in the graph")

        nodes = nodes + [node]
        if distance == 0:
            return nodes

        for edge in self.graph[node]:
            if edge.goal not in nodes:
                nodes = nodes + list(set(self.breadthFirst(edge.goal, distance-1, nodes)) - set(nodes))

        return nodes


class NetworkError(Exception):
    def __init__(self, message):
        super(NetworkError, self).__init__(message)










