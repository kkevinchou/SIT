#205 lines of code
import pygame
import random
from pygame.locals import *
from pyCanvas import *
from pyCursors import *

pygame.init()
screen_w,screen_h = (1024,768)
display_info = pygame.display.Info()
monitor_w = display_info.current_w
monitor_h = display_info.current_h
pygame.display.quit()
center_win = str(monitor_w/2-screen_w/2)+","+str(monitor_h/2-screen_h/2)
os.environ['SDL_VIDEO_WINDOW_POS'] = center_win
screen = pygame.display.set_mode((screen_w,screen_h))
clock = pygame.time.Clock()
SCREEN_REFRESH = pygame.USEREVENT
pygame.time.set_timer(SCREEN_REFRESH, int(1000.0/35))
pygame.display.set_caption('PyMap v0.9.4 - 2D Tile Mapping')

#check for basic folder structure
cwd = os.getcwd()
dir_lst = os.listdir(cwd)
if 'Maps' not in dir_lst:
        os.mkdir(cwd+'\\Maps')
if 'Tilesets' not in dir_lst:
        os.mkdir(cwd+'\\Tilesets')
        os.mkdir(cwd+'\\Tilesets\\Default')
        
class pyMain:
        def __init__(self):
                self.canvas = Canvas((32,32),(24,22))
                set_cursor_from_image('crosshair_cursor.png', (11,11))
                self.running = True
        def handle_events(self):
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                        msg = None
                        if self.canvas.tell:
                                msg = self.canvas.tell.pop(0)
                                if "loadmap:" in msg:
                                        map_to_load = msg.split(":")[1]
                                        new_map = Canvas.load(map_to_load, screen, self.canvas)
                                        if new_map:
                                                self.canvas = new_map
                                        continue
                                if "tileobj:" in msg:
                                        obj = msg.split(":")[1]
                                        self.canvas.selected_tile_obj = obj
                                        continue
                                if "loadtileset:" in msg:
                                        tileset_to_load = msg.split(":")[1]
                                        self.canvas.load_tileset(tileset_to_load)
                                        continue
                        if event.type == pygame.QUIT:
                                self.running = False
                                return
                        if event.type == MOUSEBUTTONUP:
                                pressed_keys = pygame.key.get_pressed()
                                if self.canvas.active_menu:
                                        self.canvas.menus[self.canvas.active_menu].check_click(pos,True)
                                        self.canvas.active_menu = None
                                        pygame.event.clear()
                                        continue
                                if not self.canvas.view_rect.collidepoint(pos):
                                        if self.canvas.select_point1:
                                                self.canvas.clear_points()
                                        if not self.canvas.tile_selector.view_rect.collidepoint(pos):
                                                for btn in self.canvas.buttons:
                                                        btn.check_click(pos, True)
                                                for btn in self.canvas.show_layer_buttons:
                                                        btn.check_click(pos, True)
                                                for btn in self.canvas.edit_layer_buttons:
                                                        btn.check_click(pos, True)
                                if event.button == 1:#left mb
                                        if self.canvas.view_rect.collidepoint(pos):
                                                if self.canvas.select_point1:
                                                        if pressed_keys[pygame.K_LSHIFT]:
                                                                self.canvas.invert_selection = True
                                                                self.canvas.select_point(pos)
                                                        else:
                                                                self.canvas.select_point(pos)
                                if event.button == 3:#right mb
                                        if self.canvas.view_rect.collidepoint(pos):
                                                if self.canvas.select_point1:
                                                        self.canvas.deselect_selection = True
                                                        self.canvas.select_point(pos)
                        if event.type == KEYDOWN or event.type == KEYUP or msg:
                                pressed_keys = pygame.key.get_pressed()
                                self.canvas.fill_ordered = pressed_keys[pygame.K_LSHIFT]
                                self.canvas.tile_selector.add_to_selected = pressed_keys[pygame.K_LSHIFT]
                                if event.type == KEYUP:
                                        continue
                                if pressed_keys[pygame.K_ESCAPE]:
                                        if self.canvas.active_menu:
                                                self.canvas.menus[self.canvas.active_menu].close()
                                                self.canvas.active_menu = None
                                                pygame.event.clear()
                                                continue
                                        if self.canvas.selected_tile_obj:
                                                self.canvas.selected_tile_obj = None
                                                continue
                                        if self.canvas.selected_cells:
                                                self.canvas.clear_selected()
                                                self.canvas.invert_selection = False
                                        #else:
                                                #self.running = self.canvas.quit_app_prompt(screen)
                                if pressed_keys[pygame.K_UP]:
                                        self.canvas.change_view((0,-1))
                                if pressed_keys[pygame.K_DOWN]:
                                        self.canvas.change_view((0,1))
                                if pressed_keys[pygame.K_LEFT]:
                                        self.canvas.change_view((-1,0))
                                if pressed_keys[pygame.K_RIGHT]:
                                        self.canvas.change_view((1,0))
                                if pressed_keys[pygame.K_c]:
                                        if pressed_keys[pygame.K_LSHIFT] and not pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.insert_col()
                                        if not pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.remove_col()
                                if pressed_keys[pygame.K_r]:
                                        if pressed_keys[pygame.K_LSHIFT] and not pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.insert_row()
                                        if not pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.remove_row()
                                if pressed_keys[pygame.K_x]:
                                        if pressed_keys[pygame.K_LSHIFT] and not pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.expand()
                                        if not pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.shrink()
                                if pressed_keys[pygame.K_f]:
                                        self.canvas.fill_selected()
                                if pressed_keys[pygame.K_F1]:
                                        print('Would make image of entire map')
                                        #self.canvas.export_to_img()
                                if pressed_keys[pygame.K_s] or msg == 'saveas':
                                        if pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_LCTRL] or msg == 'saveas':
                                                self.canvas.save_as_prompt(screen)
                                        if not pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_LCTRL]:
                                                self.canvas.save()
                                if pressed_keys[pygame.K_t] and pressed_keys[pygame.K_LSHIFT]:
                                        self.canvas.refresh_tileset()
                                        continue
                                if pressed_keys[pygame.K_t] or msg == 'loadtileset':
                                        tileset_names = os.listdir(os.getcwd()+'\\Tilesets')
                                        self.canvas.menus['tileset_list_menu'] = ItemList_Menu(self.canvas, (138,768-25), 'loadtileset')
                                        self.canvas.menus['tileset_list_menu'].add_menu_items(tileset_names)
                                        self.canvas.menus['tileset_list_menu'].open = True
                                        self.canvas.active_menu = 'tileset_list_menu'
                                        continue
                                if pressed_keys[pygame.K_m]:
                                        self.canvas.make_object_prompt(screen)
                                if pressed_keys[pygame.K_z]:
                                        self.canvas.set_z_val(self.canvas.get_z_prompt(screen))
                                if pressed_keys[pygame.K_SPACE]:
                                        self.canvas.clear_selected_contents()
                                if pressed_keys[pygame.K_n] or msg == 'newmap':
                                        new_canvas = Canvas.new_map_prompt(screen, self.canvas)
                                        if new_canvas:
                                                del self.canvas
                                                self.canvas = new_canvas
                                        pygame.event.clear()
                                        return
                                if pressed_keys[pygame.K_l] or msg == 'loadmap':
                                        map_names = os.listdir(os.getcwd()+'\\Maps')
                                        self.canvas.menus['map_list_menu'] = ItemList_Menu(self.canvas, (0,768-25), 'loadmap')
                                        self.canvas.menus['map_list_menu'].add_menu_items(map_names)
                                        self.canvas.menus['map_list_menu'].open = True
                                        self.canvas.active_menu = 'map_list_menu'
                                        continue
                                if pressed_keys[pygame.K_o] or msg == 'object_menu':
                                        object_names = self.canvas.tile_obj_list.keys()
                                        if not object_names:
                                                continue
                                        self.canvas.menus['tile_object_menu'] = ItemList_Menu(self.canvas, (345, 768-25), 'tileobj')
                                        self.canvas.menus['tile_object_menu'].add_menu_items(object_names)
                                        self.canvas.menus['tile_object_menu'].open = True
                                        self.canvas.active_menu = 'tile_object_menu'
                        if event.type == MOUSEBUTTONDOWN:
                                pressed_keys = pygame.key.get_pressed()
                                if event.button == 1:#left mb
                                        if self.canvas.active_menu:
                                                self.canvas.menus[self.canvas.active_menu].check_click(pos)
                                                pygame.event.clear()
                                                continue
                                        if self.canvas.view_rect.collidepoint(pos):
                                                self.canvas.select_point(pos)
                                                continue
                                        if self.canvas.tile_selector.view_rect.collidepoint(pos):
                                                self.canvas.tile_selector.select_tile(pos)
                                                if pressed_keys[pygame.K_LCTRL]:
                                                        if pressed_keys[pygame.K_LSHIFT]:
                                                                #may not be correctly handled
                                                                self.canvas.clear_selected()
                                                        self.canvas.select_cells_from_tileset()
                                                continue
                                        for btn in self.canvas.buttons:
                                                btn.check_click(pos)
                                        for btn in self.canvas.show_layer_buttons:
                                                btn.check_click(pos)
                                        for btn in self.canvas.edit_layer_buttons:
                                                btn.check_click(pos)
                                if event.button == 3:#right mb
                                        if self.canvas.view_rect.collidepoint(pos):
                                                self.canvas.select_point(pos)
                                                continue
                                        if self.canvas.tile_selector.view_rect.collidepoint(pos):
                                                self.canvas.tile_selector.clear_selected(pos)
                                                continue
                                if event.button == 5:#mid wheel down mb
                                        if self.canvas.tile_selector.view_rect.collidepoint(pos):
                                                if pressed_keys[pygame.K_LSHIFT]:
                                                        self.canvas.tile_selector.scroll_tiles((1,0))
                                                else:
                                                        self.canvas.tile_selector.scroll_tiles((0,1))
                                                continue
                                        if self.canvas.view_rect.collidepoint(pos):
                                                if pressed_keys[pygame.K_LSHIFT]:
                                                        self.canvas.change_view((1,0))
                                                else:
                                                        self.canvas.change_view((0,1))
                                                continue
                                if event.button == 4:#mid wheel up mb
                                        if self.canvas.tile_selector.view_rect.collidepoint(pos):
                                                if pressed_keys[pygame.K_LSHIFT]:
                                                        self.canvas.tile_selector.scroll_tiles((-1,0))
                                                else:
                                                        self.canvas.tile_selector.scroll_tiles((0,-1))
                                                continue
                                        if self.canvas.view_rect.collidepoint(pos):
                                                if pressed_keys[pygame.K_LSHIFT]:
                                                        self.canvas.change_view((-1,0))
                                                else:
                                                        self.canvas.change_view((0,-1))
                                                continue
                                if event.button == 2:
                                        self.canvas.snap_view(pos)
                        if event.type == SCREEN_REFRESH:
                                screen.fill((0,0,0))
                                self.canvas.update()
                                self.canvas.draw(screen)
        def run(self):
                while self.running:
                        self.handle_events()
                        pygame.display.flip()
                pygame.quit()
