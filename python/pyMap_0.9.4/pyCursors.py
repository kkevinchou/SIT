#31 lines of code (7/21/2012)
import pygame
import os

#the images size must be a multiple of 8
#the image must contain only 3 colors
#(0,0,0)black, (255,255,255)white, (255,0,255)tranparent(pink)
def set_cursor_from_image(image, hotspot = (0,0)):
    #if os.path.isfile((cwd+'/'+image)):
    img = pygame.image.load(image).convert()
    w,h = img.get_size()
    strings = []
    size = (w,h)
    if w%8 == 0 and h%8 == 0:
        black = pygame.Color(0,0,0,255)
        white = pygame.Color(255,255,255,255)
        trans = pygame.Color(255,0,255,255)
        img.lock()
        for r in range(0, w):
            pix_str = ""
            for c in range(0, h):
                color = img.get_at((r,c))
                if color == white:
                    pix_str += 'X'
                if color == black:
                    pix_str += '.'
                if color == trans:
                    pix_str += ' '
            strings.append(pix_str)
        img.unlock()
        new_cursor = pygame.cursors.compile(strings)
        pygame.mouse.set_cursor(size, hotspot, *new_cursor)
                
    
