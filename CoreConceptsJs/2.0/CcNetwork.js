/**
 * JavaScript implementation of the core concept 'network'.
 * version: 2.0.0
 * (c) Liangcun Jiang
 * latest change: July 28, 2017.
 */
define([
    "dojo/_base/declare",
    "lib/jsnetworkx"
], function (declare, jsnx) {
    //null signifies that this class has no classes to inherit from
    return declare(null, {
        /**
         *Network constructor: Constructs a CcNetwork instance
         *@param nodeData: an array of nodes with optional attributes, e.g. [0,[1, {size: 8}],2]
         *@param edgeData: an array of edges with optional lables, e.g. [[0, 1], [2, 1, {distance: 5}]]
         */
        constructor: function (nodeData, edgeData) {
            this._G = new jsnx.DiGraph();
            this._G.addNodesFrom(nodeData);
            this._G.addEdgesFrom(edgeData);
        },

        /**
         * Network function: returns a copy of the graph nodes in a list
         *  Return type: [node]
         */
        nodes: function () {
            //return this._G.nodes(true);
            return this._G.nodes();
        },

        /**
         * Network function: returns list of edges
         * Return type: Array [edge]
         */
        edges: function () {
            return this._G.edges();
        },

        /**
         * Network function: Adds a node with the attributes attr
         * @param node: node value
         * @param attr: node attributes in form of key/value pairs {k1: v1, k2: v2}
         * Return type: CcNetwork
         */
        addNode: function (node, attr) {
            this._G.addNode(node, attr);
        },

        /**
         * Network function: Adds an edge with the attributes attr between node u and v
         * @param attr: node attributes in form of key/value pairs {k1: v1, k2: v2}
         * Return type: CcNetwork
         */
        addEdge: function (u, v, attr) {
            this._G.addEdge(u, v, attr);
        },

        /**
         * Network function: returns whether node v can be reached from node u
         *  Return type: Boolean
         */
        connected: function (u, v) {
            return jsnx.hasPath(this._G, {source: u, target: v});
        },

        /**
         * Network function: returns shortest path in the network from node source to node target
         * Return type: Array [edge]
         */
        shortestPath: function (source, target) {
            return jsnx.shortestPath(this._G, {source: source, target: target});
        },

        /**
         * Network function: returns number of edges to other nodes
         * Return type: Int
         */
        degree: function (node) {
            return this._G.degree(node);
        },

        /**
         * Network function: returns the length of the shortest path from the source to the target
         * Return type: Int
         */
        distance: function (source, target) {
            return jsnx.shortestPathLength(this._G, {source: source, target: target});
        },

        /**
         * Network function: returns all nodes within the distance from a node in this network
         * Return type: Array [node]
         */
        breadthFirst: function (node, distance) {
            var map = jsnx.singleSourceShortestPath(this._G, node, distance);
            return Array.from(map.keys());
        }
    });
});
