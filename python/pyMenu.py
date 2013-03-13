from os import getcwd, listdir
from os.path import join
import sys
import pygame
import globalvars
from pygame.locals import *

def title():
    globalvars.screen.fill((0,0,0))
    menu = Menu()
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(64)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional
    menu.init(['Start','Options','Quit'])#necessary
    #menu.move_menu(0, 0)#optional
    menu.draw()
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1)
                if event.key == K_DOWN:
                    menu.draw(1)
                if event.key == K_RETURN:
                    if menu.get_position() == 2:
                        pygame.display.quit()
                        sys.exit()
                    elif menu.get_position() == 0:
                        return;
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        globalvars.clock.tick(globalvars.FPS)  


class Menu:
    menuItems = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    menuItemsLength = 0
    kolor_tla = (51,51,51)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    itemSelection = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection
        
    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.itemSelection
    
    def init(self, menuItems):
        self.menuItems = menuItems
        self.menuItemsLength = len(self.menuItems)
        self.createStructures()        
        
    def draw(self,przesun=0):
        if przesun:
            self.itemSelection += przesun 
            if self.itemSelection == -1:
                self.itemSelection = self.menuItemsLength - 1
            self.itemSelection %= self.menuItemsLength
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.itemSelection].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in range(self.menuItemsLength):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        globalvars.screen.blit(menu,self.pozycja_wklejenia)
        return self.itemSelection

    def createStructures(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in range(self.menuItemsLength):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.menuItems[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2            
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = globalvars.screen.get_rect().centerx - self.menu_width / 2
        y = globalvars.screen.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my)

