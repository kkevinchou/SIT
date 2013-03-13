import pygame, sys, astar

from astar import AStar, SQ_MapHandler, SQ_SITMapHandler, SQ_Location
from pygame.locals import *

startpoint = [0, 0]
endpoint = [199, 0]

w = 200
h = 100

mapdata = [[1 for y in range(h)] for x in range(w)]
#mapdata[0][1] = 100

#mapdata = [x for x in range(256 * 128)]

astarAlg = AStar(SQ_SITMapHandler(mapdata, w, h))
start = SQ_Location(startpoint[0], startpoint[1])
end = SQ_Location(endpoint[0], endpoint[1])
p = astarAlg.findPath(start, end)

for i in p.getNodes():
    print(str(i.location.x) + " " + str(i.location.y))
