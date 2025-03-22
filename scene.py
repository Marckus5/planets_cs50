import pygame
from planet import Planet

class Scene():
    def __init__(self, simulation, state : int):
        self.simulation = simulation
        self.state = state


        self.surface = pygame.Surface(self.simulation.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()

        sun = Planet(self, name = "sun", mass = 10e+6, color = 'yellow', radius = 16, stationary=True)
        earth = Planet(self, name = "earth", mass = 100, color = 'blue', radius = 4)
        moon = Planet(self, name = "moon", mass = 1, color = 'grey', radius = 2)
        mars = Planet(self, name = "mars", mass = 100, color = 'red', radius = 4)
        
        earth.set_orbit(sun, 0, 300, 300, periapsisAngle= 90)
        mars.set_orbit(sun, 45, 200, 300)
        moon.set_orbit(earth, 0, 1, 1)

        sun1 = Planet(self, name = "sun1", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2 = Planet(self, name = "sun2", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2.set_orbit(sun1, 0, 100, 100)
        self.planetList.add(sun1, sun2)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

        for planet in self.planetList:
            print(planet.name + ": " + f"{planet.Position.x}, " + f"{planet.Position.y}")

        
    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)

        self.simulation.screen.blit(self.surface,(0,0))