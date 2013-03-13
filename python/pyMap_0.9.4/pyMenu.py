import pygame
from pyButtons import *

class Menu:
    def __init__(self, parent, anchor_location):
        self.parent = parent
        self.hpadding = 3#horizontal
        self.vpadding = 3#vertical
        self.anchor_x,self.anchor_y = anchor_location#left_bottom
        self.buttons = []
        self.image = None
        self.rect = None
        self.open = False
        self.item_id = 0
    def get_max_size(self):
        w = 0
        h = 0
        if self.buttons:
            for button in self.buttons:
                tmp = button.rect.w
                if tmp > w:
                    w = tmp
                h += button.rect.h + self.vpadding
        return (w,h)
    def build(self):
        w,h = self.get_max_size()
        self.image = pygame.Surface((w,h))
        self.image.fill((0,0,0))
        top = 0
        for button in self.buttons:
            self.image.blit(button.image, (0, top))
            button.x,button.y = (0,top)
            button.rect.topleft = (0,top)#update for click checking
            top += button.rect.h+self.vpadding
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.anchor_x, self.anchor_y-top)
    def check_click(self, pos, up_click = False):
        x,y = pos
        x -= self.rect.left
        y -= self.rect.top
        for button in self.buttons:
            if button.check_click((x,y), up_click):
                self.close()
    def assign_parent(self, parent):
        self.parent = parent
        if self.buttons:
            for button in self.buttons:
                button.parent = self.parent
    def add_menu_items(self, item_list):
        if item_list:
            for item in item_list:
                item.id = self.item_id
                self.buttons.append(item)
                self.item_id += 1
            self.build()
    def draw(self, surface):
        if self.image and self.open:
            w,h = self.image.get_size()
            x = self.anchor_x
            y = self.anchor_y - h
            surface.blit(self.image, (x,y))
    def close(self):
        self.open = False
        if self.buttons:
            for button in self.buttons:
                button.down_click = False

class ItemList_Menu(Menu):#type_prefix will be used to handle internal msg
    def __init__(self, parent, anchor_location, type_prefix):
        Menu.__init__(self, parent, anchor_location)
        self.font = pygame.font.SysFont('arial', 15)
        self.type_prefix = type_prefix
    def add_menu_items(self, item_list):
        tmp = []
        width = 0
        height = 0
        if item_list:
            for item in item_list:
                w,h = self.font.size(item)
                width = max(width, w)
                height = max(height, h)
            width = int(width*1.5)
            for item in item_list:
                surf = pygame.Surface((width, height))
                surf.fill((128,128,128))
                txtw, txth = self.font.size(item)
                x = (width/2) - (txtw/2)
                y = (height/2) - (txth/2)
                surf.blit(self.font.render(item, True, (255,255,255)), (x,y))
                new_item = TextItem(self.parent,(0,0), surf, item, self.type_prefix)
                new_item.rect = surf.get_rect()
                new_item.id = self.item_id
                self.buttons.append(new_item)
                self.item_id += 1
        self.build()
    def close(self):
        self.open = False
        del self.buttons
        self.buttons = []
