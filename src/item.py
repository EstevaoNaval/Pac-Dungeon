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
    
    def move(self, direction_x, direction_y):
        self.position_x += direction_x * self.speed
        self.position_y += direction_y * self.speed