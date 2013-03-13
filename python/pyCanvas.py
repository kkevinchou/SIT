#1064 lines of code (7/22/2012)
##Editor Canvas
import pygame
from pygame.locals import *
import random
import os
from pySelector import *
from pyPrompts import *
from pyMenu import *
from math import sqrt

cwd = os.getcwd()

screen_h = 768


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

#start Canvas class definition#
class Canvas:
    def __init__(self, tile_size, map_size_in_tiles):
        #--------------------------------------------#
        #temporary calculations and variable declarations#
        screen_w,screen_h = (0,0)
        if pygame.display.get_init():
            screen_w, screen_h = pygame.display.get_surface().get_size()
        tile_w, tile_h = tile_size
        map_w, map_h = map_size_in_tiles
        map_width = map_w * tile_w
        map_height = map_h * tile_h
        max_view_w = screen_w
        max_view_h = screen_h
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
        self.grid_ref = []#array for multilayer functionality
        self.tell = []#used by other objects to post messages to the canvas
        self.status_msg = []#used to show status messages
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
        self.tile_selector = Tile_Selector((self.tile_width, self.tile_height),(screen_w*0.20, screen_h*0.45),(screen_w, screen_h))
        self.add_layer((self.tile_width, self.tile_height), self.map_size_in_tiles)

        #end class properties#
        #--------------------#
    #-------------------#
    #start class function definitions#
    def draw(self, surface):
        x_offset = self.tile_view_x[0]*self.tile_width
        y_offset = self.tile_view_y[0]*self.tile_height
        x,y = (0,0)
        rect = None
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

    def post_status(self, msg):
        if len(self.status_msg) == 4:
            self.status_msg.pop(-1)
        self.status_msg.insert(0,msg)
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
        self.max_layer += 1

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
        map_file.close()
        pygame.event.clear()
        return new_canvas

    #end class methods#
    #-----------------#
#end canvas class declaration#
#<><><><><><><><><><><><><><>#
