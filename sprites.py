# Base sprites class for Flynn
class Flynn(pygame.sprite.Sprite, object):
    # Constructer
    def __init__(self, pos=(0,0)):
        pygame.sprite.Sprite.__init(self)

        # Graphic variables
        self.facing = 'front'
        self.action = 'stand' #stand, walk, throw, shoot
        self.image = globalvars.images['Flynn' + self.facing + self.action]
        
        # Position
        self.px = globalvars.screen_width/2 - self.image.get_width()/2
        self.py = globalvars.screen_height/2 - self.image.get_height()/2

        # Parameters 
        self.speed = 64

        #timers
        self.animetimer = 0
        self.itemtimer = 0

    # move
    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_a]:
            self.px-=1
            self.facing = 'left'
            self.action = 'walk'
        elif pressed[K_d]:
            self.px+=1
            self.facing = 'right'
            self.action = 'walk'
        elif pressed[K_w]:
            self.py-=1
            self.facing = 'back'
            self.action = 'walk'
        elif pressed[K_s]:
            self.py+=1
            self.facing = 'front'
            self.action = 'walk'
    
    # update
    def update(slef):
        self.image = globalvars.images['Flynn' + self.facing + self.action]
        screen.blit(self.image, (self.px, self.py))
