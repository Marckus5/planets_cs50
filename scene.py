import pygame
from planet import Planet

class Scene():
    def __init__(self, screen : pygame.Surface, state : int):
        self.screen = screen
        self.state = state


        self.surface = pygame.Surface(self.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()

        sun = Planet(self, mass = 200, color = 'yellow', radius = 16, stationary=True)
        earth = Planet(self, mass = 1, color = 'blue', radius = 4)
        mars = Planet(self, mass = 1, color = 'red', radius = 4)
        

        earth.set_orbit(sun, 0, 50, 200, periapsisAngle= 90)
        mars.set_orbit(sun, 180, 200, 300)

        self.planetList.add(sun, earth, mars)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

        for planet in self.planetList:
            #print(planet.X, planet.Y)
            #print()
            pass

        
    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)

        self.screen.blit(self.surface,(0,0))