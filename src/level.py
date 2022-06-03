from knight import Knight
from item import Item, ValuableItem

class Level:
    def __init__(self, screen, knight, list_tilemap_divided_layer, path_gem, path_valuable_item):
        # setup básico
        self.screen = screen
        self.tilemap_floor_img = list_tilemap_divided_layer[0]
        self.tilemap_bottom_monster_img = list_tilemap_divided_layer[1]
        self.tilemap_upper_monster_img = list_tilemap_divided_layer[2]

        
        self.knight = knight
        self.path_gem = path_gem
        self.path_valuable_item = path_valuable_item