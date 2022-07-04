from level import Level
import pygame

pygame.init()

class Main:
    def __init__(self):
        self.step = 1
    
    def run(self):
        for index in range(1,5):
            level = Level(self, str(index), 'M')
            level.run()

main = Main()
main.run()