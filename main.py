import pygame,sys
from pygame.locals import *
import globalvars
import images

import pathfinder.astar
import ai.ai

from ai.ai import *
from pathfinder.astar import *

pygame.init()

#sample pic
background_sample_image = "data/bg.png"
mouse_cursor_image = "data/cursor.png"

#screen config
screen_size = screen_width, screen_height = 1024, 768
screen_colorspace = 32

#basic settings
screen = pygame.display.set_mode(screen_size, 0, 32)

#assign the pictures to the variables
background = pygame.image.load(background_sample_image).convert()
mouse_cursor = pygame.image.load(mouse_cursor_image).convert_alpha()
screen.blit(background, (0,0))
images = images.loadImages()
player_left = images['FlynnWalk'][0]
player_right = images['FlynnWalk'][1]
player = player_left

#init player position
px, py = screen_width/2 - player.get_width()/2 , screen_height/2 - player.get_height()/2
pygame.mouse.set_visible(False)

# Init AI
enemyAI = AI()
enemyAI.target = (500, 500)

# Fixing the framerate
clock = pygame.time.Clock()
fps = 60

while True:
    delta_time = clock.tick(fps)

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
            px, py = mx - player.get_width()/2, my - player.get_height()/2

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
    elif pressed[K_q] or pressed[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if(px > screen_width or px < 0):
        px += [-screen_width, screen_width][px < 0]
    if (py > screen_height or py < 0):
        py += [-screen_height, screen_height][py < 0]

    enemyAI.tick(delta_time)
    print(enemyAI.position)

    # fill the background
    screen.blit(background, (0,0))
    screen.blit(player, (px,py))
    screen.blit(player, enemyAI.position)
    screen.blit(mouse_cursor, (mx, my))
    pygame.display.update()
