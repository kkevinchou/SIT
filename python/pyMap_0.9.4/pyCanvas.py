#1064 lines of code (7/22/2012)
##Editor Canvas
import pygame
from pygame.locals import *
import random
import os
from pySelector import *
from pyPrompts import *
from pyMenu import *
from pyButtons import *
from math import sqrt

cwd = os.getcwd()
os.chdir(cwd+'\\Button_Images')
#load all the button images
new_map_btn_img = pygame.image.load('new_map_btn.png')
load_map_btn_img = pygame.image.load('load_map_btn.png')
save_map_btn_img = pygame.image.load('save_map_btn.png')
save_as_map_btn_img = pygame.image.load('save_as_map_btn.png')
expand_map_btn_img = pygame.image.load('expand_map_btn.png')
shrink_map_btn_img = pygame.image.load('shrink_map_btn.png')
add_col_btn_img = pygame.image.load('add_col_map_btn.png')
add_row_btn_img = pygame.image.load('add_row_map_btn.png')
sub_col_btn_img = pygame.image.load('sub_col_map_btn.png')
sub_row_btn_img = pygame.image.load('sub_row_map_btn.png')
fill_btn_img = pygame.image.load('fill_btn.png')
load_tileset_btn_img = pygame.image.load('load_tileset_btn.png')
refresh_tileset_btn_img = pygame.image.load('refresh_tileset_btn.png')
add_layer_btn_img = pygame.image.load('add_layer_btn.png')
rem_layer_btn_img = pygame.image.load('rem_layer_btn.png')
file_menu_btn_img = pygame.image.load('file_menu_btn.png')
resize_menu_btn_img = pygame.image.load('resize_menu_btn.png')
layer_menu_btn_img = pygame.image.load('layer_menu_btn_img.png')
tileset_menu_btn_img = pygame.image.load('tileset_menu_btn_img.png')
object_menu_btn_img = pygame.image.load('object_menu_btn_img.png')
showing_layer_btn_img = pygame.image.load('showing_layer_btn.png')
hiding_layer_btn_img = pygame.image.load('hiding_layer_btn.png')
active_layer_btn_img = pygame.image.load('active_layer_btn.png')
inactive_layer_btn_img = pygame.image.load('inactive_layer_btn.png')
#change back to the base directory
os.chdir(cwd)

#populate file menu
#when populating menu objects, the position passed to a Button object will not matter
#button objects passed to menus have non-zero tuples because of the functionality of previous releases
screen_h = 768

file_menu = Menu(None, (0,screen_h-25))
file_menu_items = []
file_menu_items.append(New_Map(None, (0,0), new_map_btn_img))
file_menu_items.append(Load_Map(None, (0,0), load_map_btn_img))
file_menu_items.append(Save_Map(None, (0,0), save_map_btn_img))
file_menu_items.append(Save_As_Map(None, (0,0), save_as_map_btn_img))
file_menu.add_menu_items(file_menu_items)

#populate resize menu
resize_menu = Menu(None, (69, screen_h-25))
resize_menu_items = []
resize_menu_items.append(Remove_Row_Map(None, (0,0), sub_row_btn_img))
resize_menu_items.append(Remove_Col_Map(None, (0,0), sub_col_btn_img))
resize_menu_items.append(Shrink_Map(None, (0,0), shrink_map_btn_img))
resize_menu_items.append(Add_Row_Map(None, (0,0), add_row_btn_img))
resize_menu_items.append(Add_Col_Map(None, (0,0), add_col_btn_img))
resize_menu_items.append(Expand_Map(None, (0,0), expand_map_btn_img))
resize_menu.add_menu_items(resize_menu_items)

#populate tileset_menu
tileset_menu = Menu(None, (138, screen_h-25))
tileset_menu_items = []
tileset_menu_items.append(Load_Tileset(None, (0,0), load_tileset_btn_img))
tileset_menu_items.append(Refresh_Tileset(None, (0,0), refresh_tileset_btn_img))
tileset_menu.add_menu_items(tileset_menu_items)

#populate layer_menu
layer_menu = Menu(None, (207, screen_h-25))
layer_menu_items = []
layer_menu_items.append(Remove_Layer(None, (0,0), rem_layer_btn_img))
layer_menu_items.append(Add_Layer(None, (0,0), add_layer_btn_img))
layer_menu.add_menu_items(layer_menu_items)

#<><><><><><><><><><><><><><>#
#start Point class definition#
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get(self):
        #returns a tuple of the Points x and y properties
        return (self.x, self.y)
    @classmethod
    def dist_from_points(Point, p1,p2):
        #returns a floating point number with the straight line distance between two Point objects
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    @classmethod
    def tl_br_from_points(Point, p1, p2):
        #returns a tuple of a determined topleft Point and bottomright Point based on two Point objects
        if p1.x <= p2.x and p1.y <= p2.y:
            return (p1, p2)
        if p1.x <= p2.x and p1.y >= p2.y:
            new_p1 = Point(p1.x, p2.y)
            new_p2 = Point(p2.x ,p1.y)
            return (new_p1, new_p2)
        if p1.x >= p2.x and p1.y >= p2.y:
            return (p2, p1)
        if p1.x >= p2.x and p1.y <= p2.y:
            new_p1 = Point(p2.x, p1.y)
            new_p2 = Point(p1.x, p2.y)
            return (new_p1, new_p2)
        else:
            return (p1, p2)
    @classmethod
    def size_from_points(Point, topleft, bottomright):
        #returns a tuple (width, height) of a rectangle whos topleft and bottomright points have
        #been determined by the Point.tl_br_from_points(p1,p2) method
        return (bottomright.x - topleft.x, bottomright.y - topleft.y)
#end Point class definition#
#<><><><><><><><><><><><><>#
#<><><><><><><><><><><><><><#
#start Cell class definition#
class Cell(pygame.Rect):
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)
        self.width = width
        self.height = height
        self.z = 0
        self.color = (255,255,255)
        self.img_ref_rect = None
        self.selected = False
    def set_ref_rect(self, img_ref_rect = None):#pass a pygame.Rect
        self.img_ref_rect = img_ref_rect
    def update(self):
        pass
    def draw(self, surface, offset=(0,0)):
        x,y = offset
        pygame.draw.rect(surface, self.color, (self.topleft[0]-x-1,self.topleft[1]-y-1, self.width+1, self.height+1), 1)
#end Cell class declaration#
#<><><><><><><><><><><><><>#
#<><><><><><><><><><><><><><><><><#
#start TileObject class definition#
#this class will be used to create temporary objects from selected adjacent cells
#the object should build itself using the selected area cell references and will
#will make an image of the combined tiles in order to be placed into the cells of
#the canvas
class TileObject:
    def __init__(self, name, size = (), info = [], image = None, shape = ()):
        self.surf_w, self.surf_h = size#(width, height)
        self.name = name
        self.info =  info
        self.shape = shape#(i,j)
        self.tmp_img = image
        #self.tmp_img.convert_alpha()
        #self.tmp_img.set_alpha(128)

#<><><><><><><><><><><><><><><#
#start Canvas class definition#
class Canvas:
    def __init__(self, tile_size, map_size_in_tiles):
        #--------------------------------------------#
        #temporary calculations and variable declarations#
        self.showing_layer_btn_img = showing_layer_btn_img
        self.hiding_layer_btn_img = hiding_layer_btn_img
        self.active_layer_btn_img = active_layer_btn_img
        self.inactive_layer_btn_img = inactive_layer_btn_img
        screen_w,screen_h = (0,0)
        if pygame.display.get_init():
            screen_w, screen_h = pygame.display.get_surface().get_size()
        tile_w, tile_h = tile_size
        map_w, map_h = map_size_in_tiles
        map_width = map_w * tile_w
        map_height = map_h * tile_h
        max_view_w = int(screen_w * 0.70)
        max_view_h = screen_h - 65
        ###############################
        #   performance precaution    #
        if tile_w <= 24:
            max_view_w = int(tile_w*24)
        if tile_h <= 24:
            max_view_h = int(tile_h*24)
        #                             #
        ###############################
        if map_width > max_view_w:
            view_width = max_view_w
        else:
            view_width = map_width
        if map_height > max_view_h:
            view_height = max_view_h
        else:
            view_height = map_height
        tile_xrange_view = int(view_width/tile_w)
        tile_yrange_view = int(view_height/tile_h)
        view_rect_w = int(max_view_w/tile_w*tile_w)
        view_rect_h = int(max_view_h/tile_h*tile_h)
        #end of calculation variable declarations#
        #----------------------------------------#
        #----------------------#
        #start class properties#
        self.name = "pyMap"
        self.tileset = "default"
        self.active_menu = None
        self.tool_tip_font = pygame.font.SysFont('times new roman', 14)
        self.tool_tip = ' '
        self.buttons = []
        self.menus = {}
        self.show_layer_buttons = []
        self.edit_layer_buttons = []
        self.grid_ref = []#array for multilayer functionality
        #self.layer_buttons.append([])
        self.tell = []#used by other objects to post messages to the canvas
        self.status_msg = []#used to show status messages
        #assign file_menu parent
        file_menu.assign_parent(self)
        self.menus['file_menu'] = file_menu
        #create and add File_Menu button
        self.buttons.append(File_Menu(self,(0,screen_h-25),file_menu_btn_img))
        #assign resize_menu parent
        resize_menu.assign_parent(self)
        self.menus['resize_menu'] = resize_menu
        #create and add Resize_Menu button
        self.buttons.append(Resize_Menu(self, (69, screen_h-25),resize_menu_btn_img))
        #assign tileset_menu parent
        tileset_menu.assign_parent(self)
        self.menus['tileset_menu'] = tileset_menu
        #create and add Tileset_Menu button
        self.buttons.append(Tileset_Menu(self, (138, screen_h-25),tileset_menu_btn_img))
        #assign layer_menu parent
        layer_menu.assign_parent(self)
        self.menus['layer_menu'] = layer_menu
        #create and add Layer Menu button
        self.buttons.append(Layer_Menu(self, (207, screen_h-25),layer_menu_btn_img))
        #create and add Objects Menu button
        self.buttons.append(Object_Menu(self, (345, screen_h-25), object_menu_btn_img))
        #add map_list menu
        self.menus['map_list_menu'] = None
        #add tile_object_list menu
        self.menus['tile_object_menu'] = None
        #add tileset_list menu
        self.menus['tileset_list_menu'] = None
        #self.buttons.append(Fill(self, (268,view_rect_h+2), fill_btn_img))
        self.screen_w, self.screen_h = (screen_w, screen_h)
        self.tile_width, self.tile_height = (tile_w, tile_h)
        self.map_size_in_tiles = map_size_in_tiles
        self.tile_view_x = [0, tile_xrange_view]
        self.tile_view_y = [0, tile_yrange_view]
        self.max_tile_view_x = [0, int(max_view_w/tile_w)]#edited for correct max range (7/20/2012)
        self.max_tile_view_y = [0, int(max_view_h/tile_h)]#edited for correct max range (7/20/2012)
        self.rect = pygame.Rect(0, 0, map_width-1, map_height-1)
        self.view_rect = pygame.Rect(0, 0, view_rect_w, view_rect_h)
        self.current_layer = 0#reference active layer
        self.max_layer = 0#current number of grids in map
        self.max_num_layers = 4#maximum_number of grids allowed
        self.show_layer_list = []
        self.tile_obj_list = {}#will be a dictionary to lookup by name
        self.selected_tile_obj = None
        self.temp_select_rect = None
        self.temp_select_point = None
        self.select_point1 = None
        self.select_point2 = None
        self.selected_cells = None
        self.tile_selector = Tile_Selector((self.tile_width, self.tile_height),(screen_w*0.20, screen_h*0.45),(screen_w, screen_h))
        #self.object_selector = Object_Selector((self.tile_width, self.tile_height),(screen_w*0.18, screen_h*0.40),(screen_w, screen_h))
        self.font = pygame.font.SysFont('times new roman', 14)
        self.highlight_selected = pygame.Surface((self.tile_width, self.tile_height)).convert_alpha()
        self.highlight_selected.fill((128,128,128,128))
        self.add_layer((self.tile_width, self.tile_height), self.map_size_in_tiles)
        #pyCanvas OPTIONS#
        #Fill a selected area with ordered tiles selected in Selector
        self.fill_ordered = False#toggled with K_LSHIFT
        #inverts a selection area(toggled with K_LSHIFT) - is applied with Left mouse clicks
        self.invert_selection = False
        self.deselect_selection = False
        #end class properties#
        #--------------------#
    #-------------------#
    #start class function definitions#
    def check_adjacent_cells(self):
        col_list = []
        row_list = []
        for item in self.selected_cells:
            col,row = item
            col_list.append(col)
            row_list.append(row)
        for i in range(min(col_list), max(col_list)+1, 1):
            for j in range(min(row_list),max(row_list)+1, 1):
                if (i,j) not in self.selected_cells:
                    print('cells not adjacent')
                    return False
                if not self.grid_ref[self.current_layer][i][j].img_ref_rect:
                    print('all cells must have a reference to a tile')
                    return False
        return True
    def make_object(self, name):
        #canvas, adjacent_cells = [], name = 'New', tsize = (0,0), tset = None
        if name in self.tile_obj_list.keys():
            print('tile object with name', name, 'exists')
            return False
        img_ref_start = min(self.selected_cells)
        img_ref_end = max(self.selected_cells)
        tiles_wide = (img_ref_end[0]-img_ref_start[0]+1)
        tiles_high = (img_ref_end[1]-img_ref_start[1]+1)
        surf_w = tiles_wide * self.tile_width
        surf_h = tiles_high  * self.tile_height
        tmp_img = pygame.Surface((surf_w,surf_h))
        layer = self.current_layer
        info = []
        i = 0
        for col in range(img_ref_start[0], img_ref_end[0]+1, 1):
            j = 0
            for row in range(img_ref_start[1], img_ref_end[1]+1, 1):
                ref_rect = pygame.Rect(self.grid_ref[layer][col][row].img_ref_rect)
                tmp_img.blit(self.tile_selector.tilesheet, (i*self.tile_width, j*self.tile_height), ref_rect)
                info.append((i,j,ref_rect))
                j += 1
            i += 1
        shape = (i,j)
        tmp_img.convert_alpha()
        tmp_img.set_alpha(128)
        self.tile_obj_list[name] = TileObject(name, (surf_w,surf_h), info, tmp_img, shape)
        self.save_objects()
        self.clear_selected()
        return True
    def load_object(self, name, size, info, shape):
        converted_info = []
        object_ok = True
        tmp_img = pygame.Surface(size)
        for item in info:
            col,row,left,top,width,height = item.split(',')
            col = int(col)
            row = int(row)
            left = int(left.strip('<rect('))
            top = int(top)
            width = int(width)
            height = int(height.strip(')>'))
            if (width,height) != (self.tile_width,self.tile_height):
                object_ok = False
                break
            rect = pygame.Rect(left,top,width,height)
            converted_info.append((col,row,rect))
            tmp_img.blit(self.tile_selector.tilesheet, (col*width,row*height),rect)
        tmp_img.convert_alpha()
        tmp_img.set_alpha(128)
        if not object_ok:
            self.post_status('Object Not Compatible with Map')
            return
        self.tile_obj_list[name] = TileObject(name, size, converted_info, tmp_img, shape)
    def make_object_prompt(self, surface):
        if not self.selected_cells:
            print('no cells selected')
            return
        if not self.tile_selector.tilesheet:
            print('no tilesheet loaded')
            return
        if not self.check_adjacent_cells():
            return
        size = (250, 50)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx,posy), size, 'Create New Tile Object')
        prompt.text_boxes.append(Text_Box((posx+55, posy+20), (150, 16), 'Name', 'all'))
        name = prompt.run(surface)
        if name:
            if self.make_object(name):
                self.selected_tile_obj = name
    def update(self):
        if self.select_point1:
            self.select_area_rect()
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update()
        for button in self.show_layer_buttons:
            button.update()
        for button in self.edit_layer_buttons:
            button.update()
    def draw(self, surface):
        #pygame.draw.rect(surface, (0,0,0), self.view_rect, 0)
        x_offset = self.tile_view_x[0]*self.tile_width
        y_offset = self.tile_view_y[0]*self.tile_height
        x,y = (0,0)
        rect = None
        #pygame.draw.rect(surface, (255,255,255), self.view_rect, 1)
        selection = []
        for layer in range(0, len(self.grid_ref), 1):
            if layer not in self.show_layer_list:
                continue
            else:
                for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                        for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                            x,y = (self.grid_ref[layer][col][row].topleft[0]-x_offset, self.grid_ref[layer][col][row].topleft[1]-y_offset)
                            rect = self.grid_ref[layer][col][row].img_ref_rect
                            if self.grid_ref[layer][col][row].img_ref_rect:
                                surface.blit(self.tile_selector.tilesheet, (x,y), rect)
                            if layer == max(self.show_layer_list):#only draw grid once regardless of layers
                                self.grid_ref[layer][col][row].draw(surface, (x_offset,y_offset))
                            if self.grid_ref[layer][col][row].selected:
                                if (x,y) not in selection:
                                    selection.append((x,y))
        if selection:
            for pos in selection:
                surface.blit(self.highlight_selected, pos)
        if self.temp_select_rect:
            pygame.draw.rect(surface, (0,200,0), self.temp_select_rect, 2)
        if self.selected_tile_obj:#make the object snap to cells
            x,y = pygame.mouse.get_pos()
            if self.view_rect.collidepoint(x,y):
                x += x_offset
                y += y_offset
                stop = False
                for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                    if stop:
                        break
                    for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                        if self.grid_ref[0][col][row].collidepoint(x,y):
                            x,y = self.grid_ref[0][col][row].topleft
                            x -= x_offset
                            y -= y_offset
                            stop = True
                            break
                surface.blit(self.tile_obj_list[self.selected_tile_obj].tmp_img, (x,y))
        x,y = pygame.mouse.get_pos()
        #if self.view_rect.collidepoint(x,y):
            #pygame.draw.line(surface, (255,255,255), (x,0), (x,y-18), 1)
            #pygame.draw.line(surface, (255,255,255), (0,y), (x-18,y), 1)
            #pygame.draw.line(surface, (255,255,255), (x+18,y), (self.view_rect.right-1,y), 1)
            #pygame.draw.line(surface, (255,255,255), (x,y+18), (x,self.view_rect.bottom-1), 1)
        self.tile_selector.draw(surface)
        for button in self.buttons:
            button.draw(surface)
        for button in self.show_layer_buttons:
            button.draw(surface)
        for button in self.edit_layer_buttons:
            button.draw(surface)
        self.show_info(surface)
        if self.active_menu:
            self.menus[self.active_menu].draw(surface)
    def post_status(self, msg):
        if len(self.status_msg) == 4:
            self.status_msg.pop(-1)
        self.status_msg.insert(0,msg)
    def select_point(self, pos):
        x,y = pos
        #selects a point at the position of a mouse click
        #get the x and y offsets based on the tile_view_x and tile_view_y class properties
        x_offset = self.tile_view_x[0]*self.tile_width
        y_offset = self.tile_view_y[0]*self.tile_height
        if self.view_rect.collidepoint(x,y):
            if self.selected_tile_obj:
                w = self.tile_obj_list[self.selected_tile_obj].surf_w
                h = self.tile_obj_list[self.selected_tile_obj].surf_h
                test_x = x+x_offset
                test_y = y+y_offset
                stop = False
                for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                    if stop:
                        break
                    for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                        if self.grid_ref[0][col][row].collidepoint(test_x,test_y):
                            test_x,test_y = self.grid_ref[0][col][row].topleft
                            min_col,min_row = (test_x/self.tile_width, test_y/self.tile_height)
                            if test_x + w < (len(self.grid_ref[0])+1)*self.tile_width:
                                if test_y + h < (len(self.grid_ref[0][0])+1)*self.tile_height:
                                    info = self.tile_obj_list[self.selected_tile_obj].info
                                    for i,j,ref_rect in info:
                                        self.grid_ref[self.current_layer][i+min_col][j+min_row].img_ref_rect = ref_rect
                            stop = True
                            break
                return
            check_cells = True#provides an escape if the cell is found before the range of the search
            for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                if not check_cells:
                    break
                for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                    if not check_cells:
                        break
                    if self.grid_ref[self.current_layer][col][row].collidepoint(x+x_offset, y+y_offset):
                        if not self.select_point1:
                            self.select_point1 = Point(col, row)
                            self.temp_select_point = Point(x,y)
                        #if one point has already been selected, a second point is assigned
                        else:
                            self.select_point2 = Point(col, row)
                        check_cells = False
            if self.select_point1:
                    self.select_area_rect()
    def select_area_rect(self):
        #selects Cells in a given rect determined by two Point objects selected with mouse clicks
        #if only one point is selected the area is updated based on the current mouse position
        #input keys will execute functions on a selected area given the key is bound to a function definition
        if self.select_point2:
            if self.deselect_selection:
                self.deselect_area_rect()
                self.deselect_selection = False
                return
            #select_point1 and select_point2 are Point Objects containing the cells (col,row) location in the grid_ref
            #using Point.tl_br_from_points() will return the Points in the appropriate Topleft/Bottomright order for unpacking into tl,br
            tl,br = Point.tl_br_from_points(self.select_point1, self.select_point2)
            #add to or make a new selection list
            if not self.selected_cells:
                self.selected_cells = []
            deselect = []
            for col in range(tl.x, br.x+1, 1):
                pygame.event.pump()
                for row in range(tl.y, br.y+1, 1):
                    if (col,row) not in self.selected_cells:
                        self.grid_ref[self.current_layer][col][row].selected = True
                        self.selected_cells.append((col,row))
                        #appending another item to the list extends its length
                        #this puts the new (col,row) tuple out of range for the next elif statement
                        #to reach it and change its selected value back to False
                    elif self.invert_selection:
                        self.grid_ref[self.current_layer][col][row].selected = False
                        deselect.append((col,row))
            if deselect:
                for col,row in deselect:
                    self.selected_cells.remove((col,row))
                self.invert_selection = False
            self.selected_cells.sort()
            #set selection points back to none
            self.clear_points()
        else:
            #if there is no second point selected get a temporary sizable rect will be
            #form on the screen with the following calculations
            x,y = pygame.mouse.get_pos()
            p1 = self.temp_select_point
            p2 = Point(x,y)
            topleft, bottomright = Point.tl_br_from_points(p1, p2)#returns the Point Objects as (topleft, bottomright)
            size = Point.size_from_points(topleft, bottomright)#returns (int, int) does not return Point Objects
            if self.view_rect.collidepoint(x,y):
                self.temp_select_rect = pygame.Rect(topleft.get(), size)
    def deselect_area_rect(self):
        if self.select_point2:
            if not self.selected_cells:
                self.selected_cells = []
            tl,br = Point.tl_br_from_points(self.select_point1, self.select_point2)
            deselect = []
            for col in range(tl.x, br.x+1, 1):
                pygame.event.pump()
                for row in range(tl.y, br.y+1, 1):
                    if (col,row) in self.selected_cells:
                        self.grid_ref[self.current_layer][col][row].selected = False
                        deselect.append((col,row))
            if deselect:
                for col,row in deselect:
                    self.selected_cells.remove((col,row))
            self.selected_cells.sort()
            #set selection points back to none
            self.clear_points()
    def select_cells_from_tileset(self):
        if not self.selected_cells:
                self.selected_cells = []
        #if shift is not held down then only one tile will be selected in the Selector
        #this means the canvas' currently selected cells will be cleared
        if not self.tile_selector.add_to_selected:
                self.clear_selected()
        for col in range(len(self.grid_ref[0])):
            pygame.event.pump()
            for row in range(len(self.grid_ref[0][0])):
                if (col,row) in self.selected_cells:
                        continue
                for i in range(len(self.tile_selector.selected_tiles)):
                    tile_col, tile_row = self.tile_selector.selected_tiles[i]
                    compare_img = self.tile_selector.tiles[tile_col][tile_row].topleft
                    if self.grid_ref[self.current_layer][col][row].img_ref_rect and compare_img == self.grid_ref[self.current_layer][col][row].img_ref_rect.topleft:
                        self.grid_ref[self.current_layer][col][row].selected = True
                        self.selected_cells.append((col,row))
    def change_view(self, move):
        #changes the view range of the map by 1 tile up, down, left, or right 
        x_tiles, y_tiles = move
        tile_xrange_view = len(self.grid_ref[0])
        tile_yrange_view = len(self.grid_ref[0][0])
        if x_tiles + self.tile_view_x[0] >= 0 and x_tiles + self.tile_view_x[1] <= tile_xrange_view:
            self.tile_view_x[0] += x_tiles
            self.tile_view_x[1] += x_tiles
            if self.select_point1 and x_tiles:
                self.temp_select_point.x -= (x_tiles * self.tile_height)
        if y_tiles + self.tile_view_y[0] >= 0 and y_tiles + self.tile_view_y[1] <= tile_yrange_view:
            self.tile_view_y[0] += y_tiles 
            self.tile_view_y[1] += y_tiles
            if self.select_point1 and y_tiles:
                self.temp_select_point.y -= (y_tiles * self.tile_height)
    def snap_view(self, pos):
        #calculates a relative position from the center of the view range
        #and the calls self.change_view() the number of times the view should be shifted
        #in a determined direction
        if self.view_rect.collidepoint(pos):
            x,y = pos
            centerx, centery = self.view_rect.center
            dist_to_centerx = int((x - centerx)/self.tile_width)#in tiles
            dist_to_centery = int((y - centery)/self.tile_height)#in tiles
            x_offset = self.tile_view_x[0]*self.tile_width
            y_offset = self.tile_view_y[0]*self.tile_height
            x += x_offset
            y += x_offset
            if dist_to_centerx != 0:
                move_x = dist_to_centerx/abs(dist_to_centerx)
                for i in range(0, abs(dist_to_centerx), 1):
                    self.change_view((move_x, 0))
            if dist_to_centery != 0:
                move_y = dist_to_centery/abs(dist_to_centery)
                for i in range(0, abs(dist_to_centery), 1):
                    self.change_view((0, move_y))
    def insert_col(self):
        #inserts a new column at the end (right side) of a canvas
        cols = len(self.grid_ref[0])
        rows = len(self.grid_ref[0][0])
        x_offset = cols * self.tile_width
        for layer in range(0, self.max_layer, 1):
            new_col = []
            for row in range(0, rows, 1):
                y_offset = row * self.tile_height
                new_col.append(Cell(x_offset, y_offset, self.tile_width, self.tile_height))
            self.grid_ref[layer].append(new_col)
        if self.tile_view_x[1] < self.max_tile_view_x[1]:
            self.tile_view_x[1] += 1
        if len(self.grid_ref[0])-1 == self.tile_view_x[1]:
            self.change_view((1,0))
    def insert_row(self):
        #inserts a new row at the end (bottom) of the canvas
        cols = len(self.grid_ref[0])
        new_row = len(self.grid_ref[0][0])
        y_offset = new_row * self.tile_height
        for layer in range(0, self.max_layer, 1):
            for col in range(0, cols, 1):
                x_offset = col * self.tile_width
                self.grid_ref[layer][col].append(Cell(x_offset, y_offset, self.tile_width, self.tile_height))
        if self.tile_view_y[1] < self.max_tile_view_y[1]:
            self.tile_view_y[1] += 1
        if len(self.grid_ref[0][0])-1 == self.tile_view_y[1]:
            self.change_view((0,1))
    def expand(self):
        self.insert_col()
        self.insert_row()
    def remove_col(self):
        #remove the column at the end (right side) of the canvas
        if self.grid_ref[0]:
            cols = len(self.grid_ref[0])
            self.clear_selected()
            if cols > 1:
                for layer in range(self.max_layer-1,-1,-1):
                    self.grid_ref[layer].pop(-1)
                if cols == self.tile_view_x[1]:
                    self.tile_view_x[1] -= 1
                    if self.tile_view_x[0] >= 1:
                        self.tile_view_x[0] -= 1
    def remove_row(self):
        #remove the row at the end (bottom) of the canvas
        if self.grid_ref[0]:
            cols = len(self.grid_ref[0])
            rows = len(self.grid_ref[0][0])
            self.clear_selected()
            if rows > 1:
                for col in range(0, cols, 1):
                    for layer in range(self.max_layer-1,-1,-1):
                        self.grid_ref[layer][col].pop(-1)
                if rows == self.tile_view_y[1]:
                    self.tile_view_y[1] -= 1
                    if self.tile_view_y[0] >= 1:
                        self.tile_view_y[0] -= 1
    def shrink(self):
        #shrinks the canvas by one column and one row
        self.remove_col()
        self.remove_row()
    def clear_points(self):
        #clear points and temp data
        self.select_point1 = None
        self.select_point2 = None
        self.temp_select_point = None
        self.temp_select_rect = None
    def clear_selected(self):
        #clear areas currently selected
        if self.selected_cells and not self.select_point1:
            for i in range(0, len(self.selected_cells), 1):
                col,row = self.selected_cells.pop(0)
                self.grid_ref[self.current_layer][col][row].selected = False
        self.clear_points()
    def fill_selected(self):
        #fills a selected area with the currently selected tile if there is one
        self.clear_points()
        if self.selected_cells and self.tile_selector.selected_tiles:
            num_tiles_selected = len(self.tile_selector.selected_tiles)
            if num_tiles_selected > 1:
                if not self.fill_ordered:#Left-Shift will toggle this properties Bool Value
                    shuffle_seq = []
                    for i in range(len(self.selected_cells)):
                        shuffle_seq.append(random.randint(0, (num_tiles_selected - 1)))
                    self.fill_selected_sequence(shuffle_seq)
                else:
                    order_seq = []
                    last_col = self.selected_cells[0]
                    ref = 0
                    for col,row in self.selected_cells:
                        if col != last_col[0]:
                            last_col = (col,row)
                            ref = 0
                        if ref >= num_tiles_selected:
                            ref = 0
                        order_seq.append(ref)
                        ref += 1
                    self.fill_selected_sequence(order_seq)
            else:
                select_col, select_row = self.tile_selector.selected_tiles[0]
                for col,row in self.selected_cells:
                    self.grid_ref[self.current_layer][col][row].set_ref_rect(self.tile_selector.tiles[select_col][select_row])
    def fill_selected_sequence(self, sequence):
        #goes through the currently selected cells and puts the selected tiles sequentially in the order the tiles were selected
        for col,row in self.selected_cells:
            tile = sequence.pop(0)
            select_col, select_row = self.tile_selector.selected_tiles[tile]
            self.grid_ref[self.current_layer][col][row].set_ref_rect(self.tile_selector.tiles[select_col][select_row])
    def clear_selected_contents(self):
        #clears the references and contents of all selected cells
        if self.selected_cells:
            for col,row in self.selected_cells:
                self.grid_ref[self.current_layer][col][row].img_ref_rect = None
    def select_cell(self, pos):
        x,y = pos
        #selects a point at the position of a mouse click
        #get the x and y offsets based on the tile_view_x and tile_view_y class properties
        x_offset = self.tile_view_x[0]*self.tile_width
        y_offset = self.tile_view_y[0]*self.tile_height
        check_cells = True#provides an escape if the cell is found before the range of the search
        for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
            if not check_cells:
                break
            for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                if not check_cells:
                    break
                if self.grid_ref[self.current_layer][col][row].collidepoint(x+x_offset, y+y_offset):
                    check_cells = False
                    if self.selected_cells:
                        if (col,row) not in self.selected_cells:
                            self.selected_cells.append((col,row))
                            self.grid_ref[self.current_layer][col][row].selected = True
                    else:
                        self.selected_cells = []
                        self.selected_cells.append((col,row))
                        self.grid_ref[self.current_layer][col][row].selected = True
    def deselect_cell(self, pos):
        if not self.selected_cells:
            return
        x,y = pos
        #selects a point at the position of a mouse click
        #get the x and y offsets based on the tile_view_x and tile_view_y class properties
        x_offset = self.tile_view_x[0]*self.tile_width
        y_offset = self.tile_view_y[0]*self.tile_height
        check_cells = True#provides an escape if the cell is found before the range of the search
        for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
            if not check_cells:
                break
            for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                if not check_cells:
                    break
                if self.grid_ref[self.current_layer][col][row].collidepoint(x+x_offset, y+y_offset):
                    check_cells = False
                    if (col,row) in self.selected_cells:
                        self.selected_cells.remove((col,row))
                        self.grid_ref[self.current_layer][col][row].selected = False
    def export_to_img(self):
        #exports the map as an image
        self.save()
        self.post_status('Building Map Image...')
        cells_w, cells_h = (len(self.grid_ref[0]), len(self.grid_ref[0][0]))
        w,h = (self.tile_width * cells_w, self.tile_height * cells_h)
        img_surface = pygame.Surface((w,h)).convert()
        img_surface.fill((255,255,255))
        for layer in range(self.max_layer-1,-1,-1):
            for col in range(0, cells_w, 1):
                for row in range(0, cells_h, 1):
                    img_surface.blit(self.tile_selector.tilesheet,
                                     self.grid_ref[layer][col][row].topleft,
                                     self.grid_ref[layer][col][row].img_ref_rect)
        cwd = os.getcwd()
        os.chdir(cwd+'\\Maps\\'+self.name)
        self.post_status('Saving Map Image...')
        pygame.image.save(img_surface, self.name+'.png')
        os.chdir(cwd)
        self.post_status('Export Complete')

    def add_layer(self, tile_size = None, map_size = None):
        if self.max_layer == self.max_num_layers:
            self.post_status('Unable to add additional layers (Max = 4)')
            return
        grid = []
        if tile_size:
            tile_w, tile_h = tile_size
        else:
            tile_w, tile_h = (self.tile_width,self.tile_height)
        if map_size:
            map_w,map_h = map_size
        else:
            map_w, map_h = (len(self.grid_ref[0]),len(self.grid_ref[0][0]))
        layer_id = self.max_layer
        for col in range(map_w):
            grid.append([])
            x_offset = col*tile_w
            for row in range(map_h):
                y_offset = row*tile_h
                grid[col].append(Cell(x_offset, y_offset, tile_w, tile_h))
        self.grid_ref.append(grid)
        self.show_layer_list.append(layer_id)
        w,h = pygame.display.get_surface().get_size()
        x = w - 54
        y = self.tile_selector.view_rect.bottom + 81 + (29*(layer_id))
        self.show_layer_buttons.append(Show_Hide_Layer(self, (x,y),
                                                  self.showing_layer_btn_img,
                                                  self.hiding_layer_btn_img,
                                                  layer_id))
        self.edit_layer_buttons.append(Edit_Layer(self, (x - 27,y),
                                             self.active_layer_btn_img,
                                             self.inactive_layer_btn_img,
                                             layer_id))
        self.max_layer += 1
    def remove_layer(self):
        if self.max_layer > 1:
            if self.current_layer == self.max_layer-1:
                self.edit_layer_buttons[-2].on_click()
            self.grid_ref.pop()
            self.max_layer -= 1
            self.show_layer_buttons.pop()
            self.edit_layer_buttons.pop()
            #show layer list starts at 0 and max layer starts at 1
            if self.max_layer in self.show_layer_list:
                self.show_layer_list.remove(self.max_layer)#remove max_layer (ie: number 1) from show layer list
    def show_info(self, surface):
        #displays information about the currently loaded canvas
        view_x_pos = (self.tile_view_x[0], self.tile_view_x[1]-1)
        view_y_pos = (self.tile_view_y[0], self.tile_view_y[1]-1)
        map_size = (len(self.grid_ref[0]), len(self.grid_ref[0][0]))
        view_x_range = self.tile_view_x[1] - self.tile_view_x[0]
        view_y_range = self.tile_view_y[1] - self.tile_view_y[0]
        cells_in_view = view_x_range * view_y_range
        if self.selected_cells:
            cells_selected = len(self.selected_cells)
        else:
            cells_selected = 0
        #surface.fill((0,0,0), ((self.view_rect.right, self.view_rect.bottom-85), (190, 90)))
        if self.status_msg:
            for i in range(0,len(self.status_msg),1):
                font_w,font_h = self.font.size(self.status_msg[i])
                w,h = surface.get_size()
                x_offset = w - font_w
                y_offset = h - font_h * (i+1)
                surface.blit(self.font.render(self.status_msg[i],True, (255,255,255)), (x_offset,y_offset))
        surface.blit(self.font.render('Map Name: '+self.name, True, (255,255,255)), (self.view_rect.right, self.view_rect.bottom-96))
        surface.blit(self.font.render('Map Size: '+str(map_size), True, (255,255,255)), (self.view_rect.right, self.view_rect.bottom-80))
        surface.blit(self.font.render('X: '+str(view_x_pos), True, (255,255,255)), (self.view_rect.right,self.view_rect.bottom-32))
        surface.blit(self.font.render('Y: '+str(view_y_pos), True, (255,255,255)), (self.view_rect.right,self.view_rect.bottom-16))
        surface.blit(self.font.render('In View: '+str(cells_in_view), True, (255,255,255)), (self.view_rect.right,self.view_rect.bottom-64))
        surface.blit(self.font.render('Selected: '+str(cells_selected), True, (255,255,255)), (self.view_rect.right,self.view_rect.bottom-48))
        #w,h = surface.get_size()
        #font_w,font_h = self.tool_tip_font.size(self.tool_tip)
        #surface.blit(self.tool_tip_font.render(self.tool_tip, True, (255,255,255)), (w-font_w, h-font_h))
    def save_objects(self):
        cwd = os.getcwd()
        os.chdir(cwd+'\\Tilesets\\'+self.tileset)
        obj_file = open(self.tileset+'.tileobj', 'w')
        for k, item in self.tile_obj_list.iteritems():
            name = item.name
            width, height = (str(item.surf_w), str(item.surf_h))
            cols,rows = (str(item.shape[0]), str(item.shape[1]))
            obj_file.write('::NewObject\n')
            obj_file.write(name+'\n')
            obj_file.write(str(width)+','+str(height)+'\n')
            shape_w = str(item.shape[0])
            shape_h = str(item.shape[1])
            obj_file.write(shape_w+','+shape_h+'\n')
            obj_file.write('::Info\n')
            for col,row,rect in item.info:
                obj_file.write(str(col)+','+str(row)+','+str(rect)+'\n')
        obj_file.write('::END\n')
        obj_file.close()
        os.chdir(cwd)
    def save(self):
        if self.name == 'pyMap':
            self.post_status('The current map is a base template. Must use \'Save As\'.')
            #call save as prompt using event posting left control left shift 's'
            return
        self.post_status('Saving Map...')
        tile_size = (self.tile_width, self.tile_height)
        map_size = (len(self.grid_ref[0]), len(self.grid_ref[0][0]))
        tiles_in_selector  = []#get the file name
        cell_info = []
        for layer in range(len(self.grid_ref)):
            for col in range(len(self.grid_ref[layer])):
                for row in range(len(self.grid_ref[layer][col])):
                    if self.grid_ref[layer][col][row].img_ref_rect:
                        cell_info.append((layer,self.grid_ref[layer][col][row].img_ref_rect, col, row))
        cwd = os.getcwd()
        os.chdir(cwd+'\\Maps\\'+self.name)
        file_name = open(self.name+'.txt', 'w')
        file_name.write(str(self.max_layer)+'\n')
        file_name.write(str(tile_size[0])+','+str(tile_size[1])+'\n')
        file_name.write(str(map_size[0])+','+str(map_size[1])+'\n')
        file_name.write('::Tileset\n')
        file_name.write(self.tileset+'\n')#tileset directory name
        file_name.write('::CellInfo\n')
        for layer, img_ref_rect, col, row in cell_info:
            topleft = img_ref_rect.topleft
            z = self.grid_ref[layer][col][row].z
            file_name.write(str(layer) + ',' + str(topleft[0]) + ',' + str(topleft[1]) + ',' +
                            str(col) + ',' + str(row) + ',' + str(z) + '\n')
        file_name.write('::END\n')
        file_name.close()
        os.chdir(cwd)
        if self.tile_obj_list:
            self.save_objects()
        self.post_status('Map Saved')
    @classmethod
    def load(self, folder, screen = None, caller = None):
        if screen:
                screen.fill((0,0,0))
                pygame.display.flip()
        cwd = os.getcwd()
        if caller:
                caller.post_status(cwd+'\\Maps\\'+folder)
        if not os.path.isdir(cwd+'\\Maps\\'+folder):
            if caller:
                caller.post_status(folder + ' folder does not exist')
            return None
        os.chdir(cwd+'\\Maps\\'+folder)
        if not os.path.isfile(cwd+'\\Maps\\'+folder+'\\'+folder+'.txt'):
            os.chdir(cwd)
            if caller:
                caller.post_status(folder + ' file does not exist')
            return None
        map_file = open(folder+'.txt')
        loading = True
        grid_layers = None
        tile_width = None
        tile_height = None
        map_width_in_tiles = None
        map_height_in_tiles = None
        grid_layers = int(map_file.readline().strip('\n'))
        tile_size = map_file.readline()
        tile_size = tile_size.strip('\n')
        tile_width, tile_height = tile_size.split(',')
        map_size = map_file.readline().strip('\n')
        map_dir = os.getcwd()
        ####################################################################################################
        os.chdir(cwd)#For the canvas to initialize properly the current directory must be changed back to the base working directory
        ##############This is to ensure the button images are loaded (7/20/2012)
        map_width_in_tiles, map_height_in_tiles = map_size.split(',')
        new_canvas = Canvas((int(tile_width), int(tile_height)), (int(map_width_in_tiles), int(map_height_in_tiles)))
        os.chdir(map_dir)#For the rest of the files to be read, the current directory must be changed back to the Maps directory (7/20/2012)
        ####################################################################################################
        new_canvas.name = folder
        check_tileset = map_file.readline().strip('\n')#should be ::Tileset
        if not check_tileset == '::Tileset':
            os.chdir(cwd)
            if caller:
                caller.post_status('Invalid map file format - Missing ::Tileset')
            return None
        tileset_dir = map_file.readline().strip('\n')#should be the folder name the tiles are stored in
        new_canvas.tileset = tileset_dir
        default_dir = cwd+'\\Tilesets\\'+'default'
        tileset_dir = cwd+'\\Tilesets\\'+tileset_dir
        if not os.path.isdir(tileset_dir):#see if the tileset folder exists
            if not os.path.isdir(default_dir):
                os.mkdir(default_dir)#create a Default folder if one does not exist
                new_canvas.tileset = 'default'
                new_canvas.post_status('Creating default Tileset Folder')
            tileset_dir = default_dir
        os.chdir(tileset_dir)
        tilesheet = os.listdir(os.curdir)
        if not new_canvas.tile_selector.load_tilesheet(tilesheet[0]):
            self.post_status('Map Tile Size Mismatch: Check Tilesheet Dimensions')
            return None
        #if everything went well up to this point, the tile objects can be loaded (located in Tileset/<name_of_tileset> folder
        next_line = map_file.readline().strip('\n')#should be ::CellInfo
        if not next_line == '::CellInfo':
            os.chdir(cwd)
            if caller:
                caller.post_status('Invalid map file format - Missing ::CellInfo')
            return None
        next_line = map_file.readline().strip('\n')
        flagged_tiles = []
        for i in range(0, grid_layers-1, 1):
            new_canvas.add_layer((int(tile_width),int(tile_height)),(int(map_width_in_tiles),int(map_height_in_tiles)))
        while next_line != '::END':
            layer, top, left, cell_col, cell_row, z = next_line.split(',')#read image name, column and row position, and z data
            layer = int(layer)
            topleft = (int(top),int(left))
            size = (int(tile_width), int(tile_height))
            col = int(cell_col)
            row = int(cell_row)
            if new_canvas.tile_selector.tilesheet_rect.collidepoint(topleft):
                new_canvas.grid_ref[layer][col][row].img_ref_rect = pygame.Rect(topleft, size)
                new_canvas.grid_ref[layer][col][row].z = int(z)
            next_line = map_file.readline().strip('\n')
        os.chdir(cwd)
        #added for loading tile objects (the above loading operation uses the tileselector directly)
        new_canvas.load_tileset(new_canvas.tileset)
        map_file.close()
        pygame.event.clear()
        new_canvas.post_status('Map Generation Complete')
        return new_canvas
    def save_as_prompt(self, surface):
        cwd = os.getcwd()
        size = (250, 50)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx,posy), size, 'Save Map As')
        prompt.text_boxes.append(Text_Box((posx+55, posy+20), (150, 16), 'Name', 'all'))
        name = prompt.run(surface)
        if name:
            if name.lower() == 'pymap':
                self.post_status('SAVE FAILED: \'pyMap\' is a reserved map name')
                return
            if os.path.isdir(cwd+'\\Maps\\'+name):
                self.post_status('SAVE FAILED: The name provided is already in use by another map')
                surface.fill((0,0,0))
                self.draw(surface)
                pygame.display.flip()
                self.save_as_prompt(surface)
            else:
                self.name = name
                os.mkdir(cwd+'\\Maps\\'+name)
                self.save()
    def load_tileset(self, tileset_directory):
        cwd = os.getcwd()
        os.chdir(cwd+'\\Tilesets')
        if not os.path.isdir(tileset_directory):#see if the tileset folder exists
            os.chdir(cwd)
            self.post_status('This should be the name of a folder inside the Tilset directory')
            self.post_status('Tileset Directory: ' +'\' '+tileset_directory.upper()+' \'' + ' Not Found')
            return
        self.post_status('Loading Tileset')
        self.tileset = tileset_directory
        os.chdir(tileset_directory)
        tile_list = os.listdir(os.curdir)
        tile_list.sort()
        loadable_images = ['.jpg','.png','.gif','.bmp','.pcx','.tga','.tif','.lbm','.pbm','.xpm']
        set_loaded = False
        obj_loaded = False
        for item in tile_list:
            if '.tileobj' in item and not obj_loaded:
                obj = open(item, 'r')
                line = obj.readline().strip('\n')#should be '::NewObject'
                reading = True
                while reading:
                    if '::END' in line:
                        reading = False
                        obj_loaded = True
                        break
                    name = obj.readline().strip('\n')
                    size = obj.readline().strip('\n')
                    width,height = size.split(',')[0], size.split(',')[1]
                    shape = obj.readline().strip('\n')
                    col,row = shape.split(',')[0], shape.split(',')[1]
                    shape = (int(col),int(row))
                    info_list = []
                    adding_info = True
                    obj.readline().strip('\n')#should be ::Info
                    line = obj.readline().strip('\n')
                    while adding_info:
                        if '<rect' in line:
                            info_list.append(line)
                        else:
                            adding_info = False
                            break
                        if not '::END' in line:
                            line = obj.readline().strip('\n')
                    self.load_object(name,(int(width),int(height)),info_list, shape)
            for img_type in loadable_images:
                if set_loaded:
                    break
                if img_type in item:
                    tilesheet = item
                    if not self.tile_selector.load_tilesheet(tilesheet):
                        self.post_status('Map Tile Size Mismatch : Check Dimensions')
                        os.chdir(cwd)
                    else:
                        set_loaded = True
        os.chdir(cwd)
        self.post_status('Tileset Loaded')
    def refresh_tileset(self):
        tileset_dir = self.tileset
        cwd = os.getcwd()
        os.chdir(cwd+'\\Tilesets')
        if not os.path.isdir(tileset_dir):#see if the tileset folder exists
            os.chdir(cwd)
            self.post_status('Tileset Directory: ' +'\' '+tileset_dir.upper()+' \'' + ' Not Found')
            return
        self.tileset = tileset_dir
        os.chdir(tileset_dir)
        tile_list = os.listdir(os.curdir)
        tile_list.sort()
        tilesheet = tile_list[0]
        if not self.tile_selector.load_tilesheet(tilesheet):
            self.post_status('Unable to Refresh Tileset '+'\' '+tileset_dir.upper()+' \'')
            self.post_status('Map Tile Size Mismatch : Check Dimensions')
            os.chdir(cwd)
            return None
        os.chdir(cwd)
        self.post_status('Refreshed Tileset')
    def get_z_prompt(self, surface):
        size = (150,50)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx, posy), size, 'Set Cell Z Data')
        prompt.text_boxes.append(Text_Box((posx+75, posy+20), (10, 16), 'Z = ', 'num'))
        new_z = prompt.run(surface)
        if new_z:
            if int(new_z) < 4:
                return int(new_z)
            else:
                self.post_status('Invalid Value (0, 1, 2, or 3)')
        else:
            self.post_status('Action Canceled')
    def set_z_val(self, value):
        if self.selected_cells:
            for col,row in self.selected_cells:
                self.grid_ref[self.current_layer][col][row].z = value
            pygame.event.pump()
        else:
            self.post_status('No Cells Selected')
    def quit_app_prompt(self, surface):
        size = (150,55)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx,posy), size, 'Quit PyMap')
        text_box = Text_Box((posx+120, posy+25), (13,15), '', 'all')
        text_box.text = '[?]'
        yes_no = Text_Box((posx+105,posy+25), (13,15), 'Save Map (Y/N):', 'all')
        prompt.text_boxes.append(yes_no)
        prompt.text_boxes.append(text_box)
        save, choice = prompt.run(surface)
        if choice:
            self.post_status('Quitting PyMap')
            if self.name != 'pyMap' and save == 'y' or save == 'Y':
                self.save()
            self.post_status('Terminating Program...')
            return False
        else:
            self.post_status('Cancel Quit')
            return True   
    @classmethod
    def new_map_prompt(self, surface, caller = None):
        #caller must be a canvas
        size = (225, 115)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx,posy), size, 'Create New Map')
        prompt.text_boxes.append(Text_Box((posx+145, posy+25), (30, 16), 'Tile Width (pixels)', 'num'))
        prompt.text_boxes.append(Text_Box((posx+145, posy+45), (30, 16), 'Tile Height (pixels)', 'num'))
        prompt.text_boxes.append(Text_Box((posx+145, posy+65), (30, 16), 'Map Width (tiles)', 'num'))
        prompt.text_boxes.append(Text_Box((posx+145, posy+85), (30, 16), 'Map Height (tiles)', 'num'))
        tile_width, tile_height, map_width, map_height = prompt.run(surface)
        if not tile_width or not tile_height or not map_width or not map_height:
            #prompt will return None for all variables above if the prompt is terminated with escape (cancel)
            #if not all the field are fill out it will be canceled also
            if caller:
                caller.post_status('Canceled New Map')
            return None
        if int(tile_width) <= 0 or int(tile_height) <= 0:
            if caller:
                caller.post_status('Invalid Tile Size')
            return None
        if int(map_width) <= 0 or int(tile_height) <= 0:
            if caller:
                caller.post_status('Invalid Map Size')
            return None
        new_canvas = Canvas((int(tile_width), int(tile_height)),(int(map_width), int(map_height)))
        new_canvas.post_status('New Map Created Successfully')
        return new_canvas
    @classmethod
    def load_map_prompt(self, surface, caller = None):
        #caller must be canvas
        size = (250,50)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        posx = screen_w/2 - size[0]/2
        posy = screen_h/2 - size[1]/2
        prompt = Prompt(surface, (posx,posy), size, 'Load Map')
        prompt.text_boxes.append(Text_Box((posx+55, posy+20), (150, 16), 'Name', 'all'))
        name = prompt.run(surface)
        if not name:
            if caller:
                caller.post_status('Canceled Load Map')
            return None
        if name.lower() == 'pymap':
            if caller:
                caller.post_status('Invalid Map Name ' + '\' ' + name.upper() + ' \'')
            return None
        cwd = os.getcwd()
        if not os.path.isdir(cwd+'\\Maps\\'+name):
            if caller:
                caller.post_status('Map: ' + '\' ' + name.upper() + ' \'' + ' does not exist')
            return None
        return name
    #end class methods#
    #-----------------#
#end canvas class declaration#
#<><><><><><><><><><><><><><>#
