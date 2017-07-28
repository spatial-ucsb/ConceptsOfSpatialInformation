"""
Tests for network implementation
:author: Fenja Kollasch, 06/2017
"""
import sys
sys.path.append('../')
import networks as n
import objects as o

# Model the big dipper as unordered graph... because you can observe a constellation only from left to right... or so
big_dipper = n.AstroNetwork("big dipper")

alkaid = o.AstroObject("alkaid", lon=206.27, lat=49.18, bounding='ccs', reference='icrs')
mizar = o.AstroObject("mizar", lon=200.75, lat=54.55, bounding='ccs', reference='icrs')
alioth = o.AstroObject("alioth", lon=193.5, lat=55.57, bounding='ccs', reference='icrs')
megrez = o.AstroObject("megrez", lon=183.75, lat=57.01, bounding='ccs', reference='icrs')
phecda = o.AstroObject("phecda", lon=178.25, lat=53.41, bounding='ccs', reference='icrs')
merak = o.AstroObject("merak", lon=165.25, lat=56.22, bounding='ccs', reference='icrs')
dubhe = o.AstroObject("dubhe", lon=165.75, lat=61.41, bounding='ccs', reference='icrs')

big_dipper.addNode(alkaid)
big_dipper.addNode(mizar)
big_dipper.addNode(alioth)
big_dipper.addNode(megrez)
big_dipper.addNode(phecda)
big_dipper.addNode(merak)
big_dipper.addNode(dubhe)

# Totally absurd color object...
big_dipper.addEdge(alkaid, mizar, distance=alkaid.relation(mizar, 'distance'), color="blue")
big_dipper.addEdge(mizar, alioth, distance=mizar.relation(alioth, 'distance'), color="blue")
big_dipper.addEdge(alioth, megrez, distance=alioth.relation(megrez, 'distance'), color="blue")
big_dipper.addEdge(megrez, dubhe, distance=megrez.relation(dubhe, 'distance'), color="red")
big_dipper.addEdge(megrez, phecda, distance=megrez.relation(phecda, 'distance'), color="blue")
big_dipper.addEdge(phecda, merak, distance=phecda.relation(merak, 'distance'), color="blue")
big_dipper.addEdge(merak, dubhe, distance=merak.relation(dubhe, 'distance'), color="blue")

print("Path from Alkaid to Dubhe: {0}".format(alkaid.relation(mizar, 'distance') +
                                              mizar.relation(alioth, 'distance') +
                                              alioth.relation(megrez, 'distance') +
                                              megrez.relation(dubhe, 'distance')))

print(big_dipper.shortestPath(alkaid, dubhe, weight=('distance', 0)))
print(big_dipper.shortestPath(alkaid, dubhe, weight=('distance', 0), color=('color', 'blue')))

print("first breadth from megrez (2):")
for s in big_dipper.breadthFirst(megrez, 2):
    print(str(s))
