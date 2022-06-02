from csv import reader
from settings import TILESIZE
import pygame

# Importa o arquivo csv e o converte em uma matriz
def import_csv_to_matrix(path):
    tilemap_layer_matrix_csv = []
    with open(path, mode='r', encoding="utf-8") as csv_layer:
        csv_layer_row = reader(csv_layer, delimiter=',')
        for row in csv_layer_row:
            tilemap_layer_matrix_csv.append(list(row))
        return tilemap_layer_matrix_csv

# Importa um tileset, corta e envia para uma matriz
def import_to_cut_tileset_into_tiles(path):
    tileset = pygame.image.load(path).convert_alpha()

    num_tile_x = int(tileset.get_size()[0] / TILESIZE)
    num_tile_y = int(tileset.get_size()[1] / TILESIZE)

    cropped_tiles = []
    for row in range(num_tile_x):
        for column in range(num_tile_y):
            x, y = row * TILESIZE, column * TILESIZE

            tile = pygame.Surface((TILESIZE, TILESIZE), flags=pygame.SRCALPHA)
            tile.blit(tileset, (0,0), pygame.Rect(x, y, TILESIZE, TILESIZE))

            cropped_tiles.append(tile)

    return cropped_tiles
