import pygame
from planet import Planet

class Scene():
    def __init__(self, simulation, state : int):
        self.simulation = simulation
        self.state = state


        self.surface = pygame.Surface(self.simulation.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()

        sun = Planet(self, mass = 10e+6, color = 'yellow', radius = 16, stationary=True)
        earth = Planet(self, mass = 100, color = 'blue', radius = 4)
        moon = Planet(self, mass = 1, color = 'grey', radius = 2)
        mars = Planet(self, mass = 100, color = 'red', radius = 4)
        
        earth.set_orbit(sun, 0, 200, 200, periapsisAngle= 90)
        mars.set_orbit(sun, 45, 200, 300)
        moon.set_orbit(earth, 0, 1, 1)

        self.planetList.add(sun, earth, moon)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

        
    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)

        self.simulation.screen.blit(self.surface,(0,0))