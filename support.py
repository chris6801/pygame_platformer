from csv import reader
import os
from os import walk
from pygame import surface
import pygame
from settings import tile_size

def get_relative_path(path: str) -> str:
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, path)


def import_csv_layout(path):
    bg_map = []
    path = get_relative_path(path)
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            bg_map.append(list(row))
        return bg_map

def import_cut_graphics(path):

    path = get_relative_path(path)
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size) 

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf
            )
    
    return cut_tiles

def import_folder(path):

    surface_list = []
    path = get_relative_path(path)

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            
    
    return surface_list