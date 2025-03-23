import pygame
from planet import Planet

class Scene():
    def __init__(self, simulation, state : int):
        self.simulation = simulation
        self.state = state


        self.surface = pygame.Surface(self.simulation.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()

        sun = Planet(self, name = "sun", mass = 10e+8, color = 'yellow', radius = 16, stationary=True)
        earth = Planet(self, name = "earth", mass = 0, color = 'blue', radius = 4)
        moon = Planet(self, name = "moon", mass = 1, color = 'grey', radius = 2)
        mars = Planet(self, name = "mars", mass = 0, color = 'red', radius = 4)

        #sun.Velocity = pygame.Vector2(10,0)
        #sun.Position.x = -100
        
        earth.set_orbit(sun, 90, 100, 200, periapsisAngle=0, retrograde=True)
        mars.set_orbit(sun, 0, 100, 200)
        moon.set_orbit(earth, 0, 1, 1)

        sun1 = Planet(self, name = "sun1", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2 = Planet(self, name = "sun2", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2.set_orbit(sun1, 0, 100, 100)
        self.planetList.add(sun, earth, mars)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

        #print(self.planetList)
        for planet in self.planetList:
            #print(planet.name + ": " + f"{planet.Position.x}, " + f"{planet.Position.y}")
            if planet.name == "earth":
                print(planet.Position.length())
                pass

        
    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)
        self.draw_orbit()

        self.simulation.screen.blit(self.surface,(0,0))

    def draw_orbit(self):
        for planet in self.planetList:
            # for stationary planets with no orbit lines
            if len(planet.orbitLine) < 2:
                continue
            pygame.draw.lines(self.surface, planet.Color, False, planet.orbitLine)


    def draw_velocity(self):
        for planet in self.planetList:
            velocityVector = (planet.Velocity) * 0.1
            velocityVector.x += 0.5*self.simulation.SCREENSIZE[0]
            velocityVector.y = -velocityVector.y + 0.5*self.simulation.SCREENSIZE[1]
            pygame.draw.line(self.surface, (255,255,255), (0,0), velocityVector, 1)