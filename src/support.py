from csv import reader
from settings import screen
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
def import_and_cut_tileset_into_tiles(path, width, height, knight_pos):
    len_sprt_x, len_sprt_y = [width, height]  # sprite size

    sprt_rect_x, sprt_rect_y = [0,0]  # where to find first sprite on sheet

    sheet = pygame.image.load(path).convert_alpha()  # Load the sheet

    sheet_rect = sheet.get_rect()  # assign a rect of the sheet's size
    sprites = []  # make a list of sprites
    for i in range(0, sheet_rect.height, height):  # rows
        for ii in range(0, sheet_rect.width, width):  # columns
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))  # clip the sprite
            sprite = sheet.subsurface(sheet.get_clip())  # grab the sprite from the clipped area
            sprites.append(sprite)  # append the sprite to the list
            sprt_rect_x += len_sprt_x  # go to the next sprite on the x axis
        sprt_rect_y += len_sprt_y  # go to the next row (y axis)
        sprt_rect_x = 0  # reset the sprite on the x axis back to 0
    return sprites  # return the sprites
