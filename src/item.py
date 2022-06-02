class Item:
    def __init__(self, path_img_item, num_point_gained, x, y):
        self.x = x
        self.y = y
        self.path_img_item = path_img_item
        self.num_point_gained = num_point_gained

    def draw(self, window):
        window.blit(self.path_img_item, (self.x,self.y))
    

class ValuableItem: