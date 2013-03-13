#195 lines of code (7/22/2012)
import pygame
from pygame.locals import *
class Button:#added 7/20/2012
    def __init__(self, parent, pos = (0,0), img = None):
        self.parent = parent
        self.image = None
        if not img:
            self.image = pygame.Surface((100,27))
            self.image.fill((200,200,200))
        else:
            self.image = img
        self.x,self.y = pos
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.tip = 'Click Me'
        self.down_click = False
        self.id = 0
    def check_click(self, pos, up_click = False):
        if not up_click:
            if self.rect.collidepoint(pos):
                self.down_click = True
            return False
        else:
            if self.down_click and self.rect.collidepoint(pos):
                self.on_click()
                self.down_click = False
                return True
            self.down_click = False
            return False
    def update(self):
        pass
    def on_click(self):
        print('clicked', self.id)
    def draw(self, surface):
        surface.blit(self.image, (self.x,self.y))

class New_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Create a New Map. [N]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.tell.append('newmap')
        #evt = pygame.event.Event(pygame.KEYDOWN, {'key':pygame.K_n})
        #pygame.event.post(evt)
class Load_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Load a Map. [L]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.tell.append('loadmap')
class Save_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Save this Map. [Left-Control][S]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.save()
class Save_As_Map(Button):#added 7/21/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Save Map As. [Left-Control][Left-Shift][S]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.tell.append('saveas')
class Expand_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Add Row and Column to Map. [Left-Shift][X]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.expand()
class Shrink_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Remove Row and Column from Map. [Left-Control][X]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.shrink()
class Add_Row_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Add Row to Map. [Left-Shift][R]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.insert_row()
class Remove_Row_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Remove Row from Map. [Left-Control][R]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.remove_row()
class Add_Col_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Add Column to Map. [Left-Shift][C]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.insert_col()
class Remove_Col_Map(Button):#added 7/20/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Remove Column from Map. [Left-Cotrol][C]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.remove_col()
class Fill(Button):#added 7/21/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
    def update(self):
        if self.parent.fill_ordered:
            self.tip = 'Fill Order. [Left-Shift][F]  '
        else:
            self.tip = 'Fill Random. [F] - More Options with [Left-Shift]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.fill_selected()
class Load_Tileset(Button):#added 7/21/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Load an Existing Tileset. [Left-Control][T]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.tell.append('loadtileset')
class Refresh_Tileset(Button):#added 7/22/2012
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Refresh Current Tileset. [Left-Shift][T]  '
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.refresh_tileset()
class Add_Layer(Button):#added 1/14/2013
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Add New Layer'
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.add_layer()
class Remove_Layer(Button):
    def __init__(self, parent, pos, img):
        Button.__init__(self, parent, pos, img)
        self.tip = 'Remove Last Layer'
    def on_click(self):
        self.parent.post_status(self.tip)
        self.parent.remove_layer()
class Show_Hide_Layer(Button):#added 1/14/2013
    def __init__(self, parent, pos, on_img, off_img, layer_id):
        Button.__init__(self, parent, pos, on_img)
        self.on_img = on_img
        self.off_img = off_img
        self.layer_id = layer_id
        self.show = True
    def update(self):
        if self.show:
            self.tip = 'Hide Layer ' + str(self.layer_id+1)
        if not self.show:
            self.tip = 'Show Layer ' + str(self.layer_id+1)
    def on_click(self):
        self.parent.post_status(self.tip)
        if self.show:
            self.parent.show_layer_list.remove(self.layer_id)
            self.image = self.off_img
            self.show = False
            return
        if not self.show:
            self.parent.show_layer_list.append(self.layer_id)
            self.image = self.on_img
            self.show = True
            return
class Edit_Layer(Button):#added 1/14/2013
    def __init__(self, parent, pos, active_img, inactive_img, layer_id):
        if parent.current_layer != layer_id:
            Button.__init__(self,parent,pos,inactive_img)
        else:
            Button.__init__(self, parent, pos,active_img)
        self.active_img = active_img
        self.inactive_img = inactive_img
        self.layer_id = layer_id
        self.tip = "Edit Layer " + str(self.layer_id+1)
    def on_click(self):
        self.parent.post_status(self.tip)
        for button in self.parent.edit_layer_buttons:
            button.image = button.inactive_img
        if self.parent.current_layer != self.layer_id:
            self.parent.clear_selected()
            self.parent.current_layer = self.layer_id
        self.image = self.active_img
class File_Menu(Button):#added 2/13/2012
    def __init__(self, parent, pos, image):
        Button.__init__(self, parent, pos, image)
    def on_click(self):
        self.parent.post_status('File Menu Open')
        self.parent.active_menu = 'file_menu'
        self.parent.menus[self.parent.active_menu].open = True
class Resize_Menu(Button):#added 2/13/2012
    def __init__(self, parent, pos, image):
        Button.__init__(self, parent, pos, image)
    def on_click(self):
        self.parent.post_status('Resize Menu Open')
        self.parent.active_menu = 'resize_menu'
        self.parent.menus[self.parent.active_menu].open = True
class Tileset_Menu(Button):#added 2/13/2012
    def __init__(self, parent, pos, image):
        Button.__init__(self, parent, pos, image)
    def on_click(self):
        self.parent.post_status('Tileset Menu Open')
        self.parent.active_menu = 'tileset_menu'
        self.parent.menus[self.parent.active_menu].open = True
class Layer_Menu(Button):#added 2/13/2012
    def __init__(self, parent, pos, image):
        Button.__init__(self, parent, pos, image)
    def on_click(self):
        self.parent.post_status('Layer Menu Open')
        self.parent.active_menu = 'layer_menu'
        self.parent.menus[self.parent.active_menu].open = True
class Object_Menu(Button):#added 2/13/2012
    def __init__(self, parent, pos, image):
        Button.__init__(self, parent, pos, image)
    def on_click(self):
        self.parent.post_status('Object Menu Open')
        self.parent.tell.append('object_menu')
class TextItem(Button):#for use in ItemMenus
    def __init__(self, parent, pos, image, ref = None, prefix = None):
        Button.__init__(self, parent, pos, image)
        self.ref = ref
        self.prefix = prefix
    def on_click(self):
        self.parent.tell.append(self.prefix+":"+self.ref)
        
        
