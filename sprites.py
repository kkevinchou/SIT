import pygame
from pygame.locals import *
import globalvars

# Base sprites class for Flynn
class Flynn(pygame.sprite.Sprite):
    # Constructer
    def __init__(self, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        # Graphic variables
        self.facing = 'Front'
        self.action = 'Stand' #stand, walk, throw, shoot
        self.image = globalvars.spreadsheetImages['Flynn' + self.facing + self.action][0]
        
        # Status
        self.px = globalvars.screen_width/2 - self.image.get_width()/2
        self.py = globalvars.screen_height/2 - self.image.get_height()/2
        self.walkFrameCount = 0;
        self.inAnime = False

        # Parameters 
        self.speed = 64

        #timers
        self.animeTimer = 0
        self.animeTimerMax = 4
        self.itemTimer = 0

    # tick the clock
    def tick(self):
        # Stand by default
        self.action = "Stand"

        if self.animeTimer == self.animeTimerMax:
            self.animeTimer = 0
        else:
            self.animeTimer += 1

        return True
        
    # animation
    def animate(self):
        # if walking
        if(self.action == "Walk"):
            # if it's the first move
            if(self.animeTimer == self.animeTimerMax * 4) :
                # re-init the count
                self.walkFrameCount = 0

            if(self.animeTimer == self.animeTimerMax) :
                self.walkFrameCount = (self.walkFrameCount + 1) % len(globalvars.spreadsheetImages['Flynn' + self.facing + self.action]) 

            self.image = globalvars.spreadsheetImages['Flynn' + self.facing + self.action][self.walkFrameCount]
            
        else:
            self.image = globalvars.spreadsheetImages['Flynn' + self.facing + self.action][0]

    # update
    def update(self):

        if not self.tick(): return

        pressed = pygame.key.get_pressed()
        if pressed[K_a]:
            self.px-=1
            self.facing = 'Left'
            self.action = 'Walk'
        elif pressed[K_d]:
            self.px+=1
            self.facing = 'Right'
            self.action = 'Walk'
        elif pressed[K_w]:
            self.py-=1
            self.facing = 'Back'
            self.action = 'Walk'
        elif pressed[K_s]:
            self.py+=1
            self.facing = 'Front'
            self.action = 'Walk'

        self.animate()
        globalvars.screen.blit(self.image, (self.px, self.py))
