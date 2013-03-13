import pygame, sys, math

from pygame.locals import *

class AI:
    position = []
    target = []
    speed = 1

    def __init__(self):
        self.position = [0, 0]

    def setTarget(self, x, y):
        self.target[0] = x;
        self.target[1] = y;

    def tick(self, delt_time):
        position = self.position
        target = self.target

        moveVec = [target[0] - position[0], target[1] - position[1]]
        magnitude = math.sqrt(moveVec[0] ** 2 + moveVec[1] ** 2)
        moveVec = [x / magnitude for x in moveVec]
        position[0] += moveVec[0]
        position[1] += moveVec[1]