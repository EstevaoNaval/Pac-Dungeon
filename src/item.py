import pygame

class Item:
    def __init__(self, path_img_item, num_earn_point, x, y):
        self.path_img_item = path_img_item
        self.num_earn_point = num_earn_point
        self.position_x = x
        self.position_y = y

    def draw(self, screen):
        screen.blit(self.path_img_item, (self.position_x, self.position_y))

    def earn_point(self, knight):
        knight.local_point += self.num_earn_point

class ValuableItem(Item):
    def __init__(self, path_img_item, num_earn_point, x, y, speed, list_direction_item):
        self.speed = speed
        self.direction = list_direction_item
        super().__init__(path_img_item, num_earn_point, x, y)
    
    def move(self, list_direction):
        self.position_x += list_direction[0] * self.speed
        self.position_y += list_direction[1] * self.speed

    def boost_hero(self, knight):
        knight.speed += 2
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        knight.speed -= 2

class Sword(Item):
    def __init__(self, path_img_item, num_earn_point, x, y):
        super().__init__(path_img_item, num_earn_point, x, y)
