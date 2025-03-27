import pygame
from planet import Planet

# TODO: camera controls: right click: drag move camera; mouse wheel: zoom
# 
class Scene():
    
    def __init__(self, simulation, state : int):
        self.simulation = simulation
        self.state = state

        self.SIZE : tuple = (self.simulation.SCREENSIZE[0] * 0.75, self.simulation.SCREENSIZE[1])
        self.surface = pygame.Surface(self.SIZE).convert()
        self.rect = self.surface.get_rect()

        self.TIMESTEP : float = 0.1 * self.simulation.DELTATIME * self.simulation.TIMESCALE

        self.planetList = CameraGroup(self)
        self.planetSelect = pygame.sprite.GroupSingle()

        sun = Planet(self, name = "sun", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        earth = Planet(self, name = "earth", mass = 10, color = 'blue', radius = 4)
        moon = Planet(self, name = "moon", mass = 0, color = 'grey', radius = 2)
        mars = Planet(self, name = "mars", mass = 0, color = 'red', radius = 4)
        
        earth.set_orbit(sun, 0, 200, 50, periapsisAngle=180, retrograde=False)
        mars.set_orbit(sun, 0, 100, 200)
        moon.set_orbit(earth, 0, 1, 1)

        sun1 = Planet(self, name = "sun1", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun2 = Planet(self, name = "sun2", mass = 10e+6, color = 'yellow', radius = 16, stationary=False)
        sun1.set_orbit(sun2, 0, 400, 200)
        sun2.set_orbit(sun1, 0, 400, 200, periapsisAngle=180)


        self.planetList.add(sun, earth)


    def run(self):
        self.planetList.update(self.planetList)


        self.surface.fill('black')
        
        self.blit_screen()
        

        
    def blit_screen(self): #NOTE always called last!!!
        self.planetList.draw(self.surface)

        pygame.draw.rect(self.surface, 'grey', self.rect, width=1)
        self.simulation.screen.blit(self.surface,(0,0))
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self, scene):
        super().__init__()

        self.Pos = pygame.Vector2(0,0)
        self.scene = scene

        self.HALFSIZE = (self.scene.SIZE[0]//2, self.scene.SIZE[1]//2)

        self.zoom : float = 1.0
        self.displaySurfaceSizeMax = pygame.Vector2(0x6bf, 0x52f)
        self.displaySurfaceSizeMin = pygame.Vector2(0x1ff, 0x1ff)

        self.displaySurfaceSize = pygame.Vector2(0x6bf, 0x52f)
        self.displaySurface : pygame.Surface = pygame.Surface(self.displaySurfaceSize, pygame.SRCALPHA)
        self.displayRect : pygame.FRect = self.displaySurface.get_frect(center = self.HALFSIZE)
        self.displayOffset = self.displaySurfaceSize // 2 - self.HALFSIZE



    def draw(self, surface : pygame.Surface):

        self.displaySurface.fill('#000020')
        #self.displaySurface.fill('grey')

        for sprite in self.sprites():
            offsetPos = sprite.rect.topleft + self.Pos + self.displayOffset

            self.displaySurface.blit(sprite.image, offsetPos)
            self.draw_orbit(self.displaySurface, sprite)

        # BUG this camera zoom consumes too much memory
        # Maybe I can dynamically change the display surface size? Limit zoom distance for now

        scaledSurface = pygame.transform.scale(self.displaySurface, self.displaySurfaceSize*self.zoom)
        scaledRect = scaledSurface.get_rect(center = self.HALFSIZE)
        surface.blit(scaledSurface, scaledRect)


    def draw_orbit(self, surface, planet):
        # for stationary planets with no orbit lines
        if len(planet.orbitLine) < 2:
            return

        offsetPos = [point + self.Pos + self.displayOffset for point in planet.orbitLine]
        
        pygame.draw.aalines(surface, planet.Color, False, offsetPos)

    def draw_velocity(self):
        for planet in self.planetList:
            velocityVector = (planet.Velocity) * 0.1
            velocityVector.x += self.planetList.HALFSIZE[0]#self.simulation.SCREENSIZE[0]
            velocityVector.y = -velocityVector.y + self.planetList.HALFSIZE[1]
            pygame.draw.line(self.surface, (255,255,255), (0,0), velocityVector, 1)