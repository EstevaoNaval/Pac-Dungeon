class Item:
    def __init__(self, path_img_item, num_earn_point, x, y):
        self.path_img_item = path_img_item
        self.num_earn_point = num_earn_point
        self.position_x = x
        self.position_y = y

    def draw(self, screen):
        screen.blit(self.path_img_item, (self.position_x, self.position_y))

class ValuableItem(Item):
    def __init__(self, path_img_item, num_earn_point, x, y, speed, direction_x, direction_y):
        self.speed = speed
        self.direction_x = direction_x
        self.direction_y = direction_y
        super().__init__(path_img_item, num_earn_point, x, y)
    
    def move(self, list_direction_item):
        self.position_x += list_direction_item[0] * self.speed
        self.position_y += list_direction_item[1] * self.speed
