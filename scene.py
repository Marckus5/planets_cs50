import pygame
from planet import Planet

# TODO: camera controls: right click: drag move camera; mouse wheel: zoom
# 
class Scene():
    def __init__(self, simulation, state : int):
        self.simulation = simulation
        self.state = state


        self.surface = pygame.Surface(self.simulation.screen.get_size()).convert()

        self.planetList = pygame.sprite.Group()
        self.cameraGroup = CameraGroup(self)

        sun = Planet(self, name = "sun", mass = 10e+8, color = 'yellow', radius = 16, stationary=False)
        earth = Planet(self, name = "earth", mass = 10, color = 'blue', radius = 4)
        moon = Planet(self, name = "moon", mass = 0, color = 'grey', radius = 2)
        mars = Planet(self, name = "mars", mass = 0, color = 'red', radius = 4)

        #sun.Velocity = pygame.Vector2(100,0)
        #sun.Position.x = -100
        
        earth.set_orbit(sun, 0, 200, 50, periapsisAngle=0, retrograde=False)
        mars.set_orbit(sun, 0, 100, 200)
        moon.set_orbit(earth, 0, 1, 1)

        sun1 = Planet(self, name = "sun1", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2 = Planet(self, name = "sun2", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2.set_orbit(sun1, 0, 100, 100)


        self.planetList.add(sun, earth)
        self.cameraGroup.add(sun, earth)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        self.blit_screen()

        #print(self.planetList)
        for planet in self.planetList:
            #print(planet.name + ": " + f"{planet.Position.x}, " + f"{planet.Position.y}")
            if planet.name == "earth":
                #print(planet.Position.length())
                pass

        
    def blit_screen(self): #NOTE always called last!!!
        #self.planetList.draw(self.surface)
        self.cameraGroup.draw(self.surface)
        

        self.simulation.screen.blit(self.surface,(0,0))

    


    def draw_velocity(self):
        for planet in self.planetList:
            velocityVector = (planet.Velocity) * 0.1
            velocityVector.x += 0.5*self.simulation.SCREENSIZE[0]
            velocityVector.y = -velocityVector.y + 0.5*self.simulation.SCREENSIZE[1]
            pygame.draw.line(self.surface, (255,255,255), (0,0), velocityVector, 1)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, scene):
        super().__init__()

        self.Pos = pygame.Vector2(100,0)

        self.rect = scene.surface.get_rect()



    def draw(self, surface : pygame.Surface):
        for sprite in self.sprites():
            offsetPos = sprite.rect.topleft + self.Pos
            surface.blit(sprite.image, offsetPos)
            self.draw_orbit(surface, sprite)


    # TODO update group, add or remove
    def updateGroup(self, planetList: pygame.sprite.Group):
        pass

    def draw_orbit(self, surface, planet):
        # for stationary planets with no orbit lines
        if len(planet.orbitLine) < 2:
            return
        offsetPos = [tuple(map(lambda a,b : a + b, point, self.Pos)) for point in planet.orbitLine]
        #print(offsetPos)
        pygame.draw.lines(surface, planet.Color, False, offsetPos)