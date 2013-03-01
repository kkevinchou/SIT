from os import getcwd, listdir
from os.path import join
from os.path import splitext
import pygame
from spritesheet import spritesheet

# Constants (would be moved to another file)
character_pixel_size = 64

# Load images from Spreadsheet
def loadImages():
    images = {}
    path = join(getcwd(), "data", "images")
    directories = listdir(path)
    for directory in directories:
        subpath = join(path, directory)
        subdirectories = listdir(subpath)
        for imagefile in subdirectories:
            # load spritesheet
            ss_image = pygame.image.load(join(subpath, imagefile))
            ss_obj = spritesheet(join(subpath, imagefile))

            frames = round(ss_image.get_height() / character_pixel_size)
            anime_set = []
            for frame in range(frames):
                image = ss_obj.image_at((0, frame * character_pixel_size, character_pixel_size, character_pixel_size))
                anime_set.append(image)

            images[directory+splitext(imagefile)[0]] = anime_set
    return images
