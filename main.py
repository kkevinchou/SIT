import pygame,sys
from pygame.locals import *
import globalvars
import images
import pyMenu
from pyCanvas import *

import pathfinder.astar
import ai.ai

from ai.ai import *
from pathfinder.astar import *

#sample pic
background_sample_image = "data/bg.png"
mouse_cursor_image = "data/cursor.png"




#assign the pictures to the variables
#background = pygame.image.load(background_sample_image).convert()
mouse_cursor = globalvars.allImages['Misccursor']
#player_left = pygame.image.load(player_sample_image_left).convert_alpha()
#player_right = pygame.image.load(player_sample_image_right).convert_alpha()
#screen.blit(background, (0,0))

player_left = globalvars.spreadsheetImages['FlynnWalk'][0]
player_right = globalvars.spreadsheetImages['FlynnWalk'][1]
player = player_left
mx, my = pygame.mouse.get_pos()

#init player position
px, py = globalvars.screen_width/2 - player.get_width()/2 , globalvars.screen_height/2 - player.get_height()/2
pygame.mouse.set_visible(False)

# Init AI
enemyAI = AI()
enemyAI.target = (500, 500)

# Fixing the framerate
clock = pygame.time.Clock()
fps = 60

pyMenu.title()

class pyMain:
    def __init__(self):
        self.canvas = Canvas((32,32),(24,22))
        self.running = True
    def handle_events(self):
        global px, py, player, mx, my
        for evt in pygame.event.get():
            #Exit event
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # update mouse cursor
            mx, my = pygame.mouse.get_pos()
            mx -= mouse_cursor.get_width()/2
            my -= mouse_cursor.get_height()/2

            if evt.type == MOUSEBUTTONDOWN:
                px = mx - player.get_width()/2
                py = my - player.get_height()/2


        pressed = pygame.key.get_pressed()
        if pressed[K_a]:
            px-=1
            player = player_left
        elif pressed[K_d]:
            px+=1
            player = player_right
        elif pressed[K_w]:
            py-=1
        elif pressed[K_s]:
            py+=1

        if(px > globalvars.screen_width or px < 0): px += [-globalvars.screen_width, globalvars.screen_width][px < 0]
        if(py > globalvars.screen_height or py < 0): py += [-globalvars.screen_height, globalvars.screen_height][py < 0]

        globalvars.screen.fill((0,0,0))
        self.canvas.draw(globalvars.screen)
        # fill the background
        #screen.blit(background, (0,0))
        globalvars.screen.blit(player, (px,py))
        globalvars.screen.blit(mouse_cursor, (mx, my))

        pygame.display.update()
        globalvars.clock.tick(globalvars.FPS / 2)


    def run(self):
        new_map = Canvas.load('dungeon', globalvars.screen, self.canvas)
        if new_map:
            self.canvas = new_map
        while self.running:
            self.handle_events()
            pygame.display.flip()
        pygame.quit()


pymap = pyMain()
pymap.run()

