import pygame,sys
from pygame.locals import *
import images
from pyCanvas import *

pygame.init()

# Screen Settings
screen_size = screen_width, screen_height = 1024, 768
screen_colorspace = 32



FPS = 30

#basic settings
screen = pygame.display.set_mode(screen_size, 0, 32)
clock = pygame.time.Clock()
SCREEN_REFRESH = pygame.USEREVENT

#screen config
screen_size = screen_width, screen_height = 1024, 768
screen_colorspace = 32

spreadsheetImages = images.loadSpreadsheetImages()
allImages = images.loadAllImages()