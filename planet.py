import pygame
from math import sin, cos, atan2, sqrt


WHITE = (255,255,255)

class Planet(pygame.sprite.Sprite):
    AU : float = 149.6e9
    G : float = 6.67428e-11
    SCALE : float = 50/AU
    TIMESTEP : float = 3600 * 24 *10

    def __init__(self, scene, mass : float, color, radius : int, posx : float, posy : float, stationary : bool = False):
        super().__init__()

        self.scene = scene
        self.WIDTH, self.HEIGHT = self.scene.screen.get_size()

        self.image = pygame.Surface((5,5), pygame.SRCALPHA)
        self.image.fill(color)
        
        
        self.rect : pygame.FRect = self.image.get_frect()

        self.X = posx
        self.Y = posy
        self.rect.center = (self.X + (self.WIDTH//2), - self.Y + (self.HEIGHT//2))
        self.Radius = radius
        self.Color = color

        self.Mass = mass
        
        self.VelocityX, self.VelocityY = 0, 0
        self.AccelerationX, self.AccelerationY = 0, 0

        self.isStationary = stationary

        self.orbitLine = []

    def draw(self, screen):
        pass

    def update(self, planets):

        for planet in planets:
            pass
        self.X += self.VelocityX
        
        
        
        self.rect.center = (self.X + (self.WIDTH//2), - self.Y + (self.HEIGHT//2))



    

        
        