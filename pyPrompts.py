#120 lines of code (7/21/2012)
import pygame
from pygame.locals import *
class Text_Box:
    def __init__(self, position = (0,0), size = (1,1), lable = 'New', input_type = 'all'):
        self.position = position
        self.lable = lable
        self.type = input_type
        self.rect = pygame.Rect((position, size))
        self.text = ''
        self.font = pygame.font.SysFont('times new roman', 12)
        self.active = False
    def draw(self, surface):
        color = (96,96,96)
        if self.active:
            color = (255,255,255)
        pygame.draw.rect(surface, color, self.rect, 0)
        w,h = self.font.size(self.lable)
        x_offset = self.rect.left - (w+5)
        surface.blit(self.font.render(self.lable, True, (0,0,0)), (x_offset, self.rect.top))
        if self.text:
            surface.blit(self.font.render(self.text, True, (0,0,0)), self.rect.topleft)
class Prompt:
    def __init__(self, surface, position, size, prompt_name = 'New Prompt', image = None):
        self.x, self.y = position
        self.name = prompt_name
        self.image = image
        self.rect = pygame.Rect((position, size))
        self.font = pygame.font.SysFont('times new roman', 16)
        self.text_boxes = []
        self.valid_list = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
        self.active_box = None
        self.running = True
        self.Shift_Down = False
    def run(self, surface):
        ret_vals = []
        if self.text_boxes and not self.active_box:
            self.active_box = self.text_boxes[0]
            self.active_box.active = True
        while self.running:
            self.process_events()
            self.draw(surface)
            pygame.display.flip()
        if self.text_boxes:
            for box in self.text_boxes:
                ret_vals.append(box.text)
        if len(ret_vals) > 1:
            return ret_vals
        else:
            return ret_vals[0]
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for box in self.text_boxes:
                    if box.rect.collidepoint(pos):
                        if self.active_box:
                            self.active_box.active = False
                        box.active = True
                        self.active_box = box
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.Shift_Down = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for box in self.text_boxes:
                        box.text = None
                    self.running = False
                    break
                if self.active_box:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_box and self.active_box.text:
                            temp = ''
                            for i in xrange(len(self.active_box.text)-1):
                                temp += self.active_box.text[i]
                            self.active_box.text = temp
                        continue
                    if event.key == pygame.K_TAB:
                        ref = 0
                        for i in xrange(len(self.text_boxes)):
                            if self.text_boxes[i] is self.active_box:
                                ref = i
                        if ref+1 > len(self.text_boxes)-1:
                            self.active_box.active = False
                            self.active_box = self.text_boxes[0]
                            self.active_box.active = True
                        else:
                            self.active_box.active = False
                            self.active_box = self.text_boxes[ref+1]
                            self.active_box.active = True
                        continue
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.Shift_Down = True
                        continue
                    if event.key == pygame.K_SPACE:
                        continue
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.running = False
                        break
                    else:
                        key_name = pygame.key.name(event.key).strip('[]')
                        if key_name not in self.valid_list:
                            continue
                        if self.active_box.type == 'all':
                            if self.Shift_Down and key_name.isalpha():
                                key_name = str.capitalize(key_name)
                            if self.Shift_Down and key_name == '-':
                                key_name = '_'
                            self.active_box.text += key_name
                        if key_name.isdigit() and self.active_box.type == 'num':
                            self.active_box.text += key_name
    def draw(self, surface):
        if self.image:
            pass
        else:
            pygame.draw.rect(surface, (192,192,192), self.rect, 0)
        w,h = self.font.size(self.name)
        cx, cy = self.rect.center
        surface.blit(self.font.render(self.name, True, (0,0,192)), (cx - int(w/2),self.rect.top))
        for box in self.text_boxes:
            box.draw(surface)
