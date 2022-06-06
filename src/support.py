from csv import reader
import codecs
from settings import TILESIZE
import pygame

# Importa o arquivo csv e o converte em uma matriz
def import_csv_to_matrix(path):
    matrix_tilemap_csv = []
    with open(path) as maze:
        labirinto_level = reader(maze, delimiter=',')
        for row in labirinto_level:
            matrix_tilemap_csv.append(list(row))
    return matrix_tilemap_csv
# Importa um tileset, corta e envia para uma matriz
def import_and_cut_tileset_into_tiles(path):
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
