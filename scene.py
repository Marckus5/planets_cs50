import pygame
from planet import Planet

class Scene():
    def __init__(self, screen : pygame.Surface, state : int):
        self.screen = screen
        self.state = state


        self.surface = pygame.Surface(self.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()

        sun = Planet(self, mass = 1.98892e30, color = 'yellow', radius = 16, posx = 0, posy = 0)
        earth = Planet(self, mass = 1.98892e30, color = 'blue', radius = 16, posx = 10, posy = 0)
        self.planetList.add(sun, earth)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)

        self.screen.blit(self.surface,(0,0))