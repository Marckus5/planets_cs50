import pygame
from math import sin, cos, atan2, sqrt


WHITE = (255,255,255)

class Planet(pygame.sprite.Sprite):
    AU : float = 149.6e9
    G : float = 6.67428e-11
    SCALE : float = 50/AU
    TIMESTEP : float = 3600 * 24 *10

    def __init__(self, scene, mass : float, color, radius : int, stationary : bool = False):
        super().__init__()

        self.scene = scene
        self.WIDTH, self.HEIGHT = self.scene.screen.get_size()

        self.image = pygame.Surface((5,5), pygame.SRCALPHA)
        self.image.fill(color)
        
        
        self.rect : pygame.FRect = self.image.get_frect()

        self.X = 0
        self.Y = 0
        self.rect.center = (self.X + (self.WIDTH//2), -self.Y + (self.HEIGHT//2))
        self.Radius = radius
        self.Color = color

        self.Mass = mass
        
        self.VelocityX, self.VelocityY = 0, 0
        self.AccelerationX, self.AccelerationY = 0, 0

        self.isStationary = stationary

        self.orbitLine = []

    def update(self, planets : pygame.sprite.Group):

        totalAccelX = totalAccelY = 0
        for planet in planets:
            if self == planet:
                    continue
            ax, ay = self.attraction(body = planet)
            totalAccelX += ax
            totalAccelY += ay
        
        self.VelocityX += -(totalAccelX)# * self.TIMESTEP)
        self.VelocityY += -(totalAccelY)# * self.TIMESTEP)
        
        self.X += self.VelocityX
        self.Y += self.VelocityY
    

        self.rect.center = (self.X + (self.WIDTH//2), -self.Y + (self.HEIGHT//2))


    def attraction(self, body):
        angle= atan2(self.Y,self.X)
        distance = sqrt((body.X - self.X)**2 + (body.Y - self.Y)**2)

        #gravitational accel
        accel = body.Mass/(distance**2)

        accelX = cos(angle) * accel
        accelY = sin(angle) * accel

        return accelX, accelY


    

        
        