#154 lines of code (7/21/2012)
import pygame
#<><><><><><><><><><><><><><#
#start Tile class definition#
class Tile(pygame.Rect):
    #a Tile is a pygame.Rect derived class that can hold a reference to a surface
    #the tile can be selected or not and will draw itself based on an offset provided
    #to it through the draw(surface, offset) method
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)
        #these values can be obtain through Rect functions but are easier to reference
        #with the obvious property names below
        self.x = x
        self.y = y
        self.selected = False
    def draw(self, surface, offset = (0,0), highlight = None):
        pass
#end Tile class definition#
#<><><><><><><><><><><><><#
class Tile_Selector:
    #the Selector class is based off the pyCanvas class but was not derived from it because
    #it must be expandable by single elements and not by entire columns and rows
    def __init__(self, tile_size = (0,0), view_size = (0,0), screen_size=(0,0)):
        #-------------------------------#
        #temporary calculation variables#
        #the parameters to this init function are precalculated and obtained by the Canvas.__init__ function
        screen_w, screen_h = screen_size
        width, height = view_size#max size the view_rect can be (a percentage of the screen width and height usually)
        tile_w, tile_h = tile_size
        tile_xrange_view = int(width/tile_w)#max number of tile columns that can fit in the desired view_size
        tile_yrange_view = int(height/tile_h)#max number of tile rows that can fit in the desired view_size
        view_rect_width = tile_xrange_view * tile_w#get the actual width of the tile viewing area
        view_rect_height = tile_yrange_view * tile_h#get the actual height of the tile viewing area
        x = screen_w - tile_xrange_view * tile_w#use to set the right of view_rect to right side of screen
        y = 0#top of view_rect to top of screen (static y position is 0)
        #end of calculation variable declarations#
        #----------------------------------------#
        #----------------------#
        #start class properties#
        self.tile_width, self.tile_height = (tile_w, tile_h)
        #get size of the rect that will enclose the selectable Tiles
        self.view_rect = pygame.Rect(x,y, view_rect_width, view_rect_height)
        #the range for which columns are to be shown
        self.max_xrange_view = tile_xrange_view#store this value in case a new tileset is loaded
        self.tile_view_x = [0,tile_xrange_view]#as with any range in Python the start is inclusive and the stop is exclusive
        #the range for which rows are to be shown
        self.max_yrange_view = tile_yrange_view#store this value in case a new tileset is loaded
        self.tile_view_y = [0,tile_yrange_view]
        #tiles currently in the Selector (2D array)
        self.tilesheet = None
        self.tilesheet_rect = None
        self.tiles = []
        #tiles currently selected
        self.selected_tiles = []
        self.highlight_selected = pygame.Surface((self.tile_width, self.tile_height)).convert_alpha()
        self.highlight_selected.fill((255,0,0,96))
        #pySelector OPTIONS#
        #add to selected tiles
        self.add_to_selected = False
        self.font = pygame.font.SysFont('times new roman', 12)
        #end class properties#
        #--------------------#
    #-------------------#
    #start class methods#
    def update(self):
        pass
    def draw(self, surface):#should check if it needs to be redrawn (when it is scrolled or a tile is selected)
        pygame.draw.rect(surface, (32,32,32), self.view_rect, 0)
        if self.tilesheet:
            x1 = self.tile_view_x[0]*self.tile_width
            y1 = self.tile_view_y[0]*self.tile_height
            surface.blit(self.tilesheet, self.view_rect.topleft, pygame.Rect(x1,y1,self.view_rect.width,self.view_rect.height))
        if self.selected_tiles:
            max_col = len(self.tiles)
            for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                if col > max_col - 1:
                    break
                for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                    if self.tiles[col][row].selected:
                        x_offset = self.view_rect.left+((col - self.tile_view_x[0])*self.tile_width)
                        y_offset = self.view_rect.top+((row - self.tile_view_y[0])*self.tile_height)
                        surface.blit(self.highlight_selected, (x_offset, y_offset))
    def load_tilesheet(self, image_name, trans = False):
        temp_sheet = pygame.image.load(image_name).convert()
        temp_sheet_rect = temp_sheet.get_rect()
        if temp_sheet_rect.width%self.tile_width or temp_sheet_rect.height%self.tile_height:
            return False
        else:
            self.clean()
            self.tilesheet = temp_sheet
            self.tilesheet_rect = temp_sheet_rect
            for col in range(0, (int)(self.tilesheet_rect.width/self.tile_width)):
                self.tiles.append([])
                for row in range(0, (int)(self.tilesheet_rect.height/self.tile_height)):
                    self.tiles[col].append(Tile(col*self.tile_width, row*self.tile_height, self.tile_width, self.tile_height))
        return True
    def select_tile(self, pos):
        if self.tiles:
            x,y = pos
            x = (x - self.view_rect.left)+(self.tile_view_x[0]*self.tile_width)
            y = (y - self.view_rect.top) +(self.tile_view_y[0]*self.tile_width)
            if not x < self.tilesheet.get_width() or not y < self.tilesheet.get_height():
                return
            check_tiles = True
            for col in range(self.tile_view_x[0], self.tile_view_x[1], 1):
                if not check_tiles:
                    break
                for row in range(self.tile_view_y[0], self.tile_view_y[1], 1):
                    if not check_tiles:
                        break
                    if self.tiles[col][row].collidepoint((x,y)):
                        check_tiles = False
                        if self.add_to_selected:
                            if (col,row) not in self.selected_tiles:
                                self.tiles[col][row].selected = True
                                self.selected_tiles.append((col,row))
                        else:
                            for (c,r) in self.selected_tiles:
                                self.tiles[c][r].selected = False
                            self.selected_tiles = []
                            self.tiles[col][row].selected = True
                            self.selected_tiles.append((col,row))
    def clear_selected(self, pos):
        if self.selected_tiles:
            x,y = pos
            check_tiles = True
            x_offset = (x - self.view_rect.left) + (self.tile_view_x[0]*self.tile_width)
            y_offset = (y - self.view_rect.top) +(self.tile_view_y[0]*self.tile_width)
            for col in range(self.tile_view_x[0], self.tile_view_x[1]):
                if not check_tiles:
                    break
                for row in range(self.tile_view_y[0], self.tile_view_y[1]):
                    if not check_tiles:
                        break
                    if self.tiles[col][row].collidepoint(x_offset, y_offset):
                        check_tiles = False
                        if (col,row) in self.selected_tiles:
                            self.tiles[col][row].selected = False
                            self.selected_tiles.remove((col,row))
    def scroll_tiles(self, direction = None):
        x_range_width = self.tile_view_x[1] - self.tile_view_x[0]
        if direction:
            col,row = direction
            if col != 0 and self.tile_view_x[1]+col <= len(self.tiles) and self.tile_view_x[0]+col >= 0:
                self.tile_view_x[0] += col
                self.tile_view_x[1] += col
            if row != 0 and self.tile_view_y[1]+row <= len(self.tiles[0]) and self.tile_view_y[0]+row >= 0:
                self.tile_view_y[0] += row
                self.tile_view_y[1] += row
    def show_info(self, surface):
        pass
    def clean(self):
        self.tile_view_x[0] = 0
        self.tile_view_x[1] = self.max_xrange_view
        self.tile_view_y[0] = 0
        self.tile_view_y[1] = self.max_yrange_view
        #added 07/21/2012
        #this functions is called when the tile_selector attempts to load a different tileset
        del self.selected_tiles
        self.selected_tiles = []
        del self.tiles
        self.tiles = []
