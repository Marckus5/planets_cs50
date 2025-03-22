import pygame
from math import sin, cos, atan2, sqrt, cos, radians


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

        self.Radius = radius
        self.Color = color
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        
        self.rect : pygame.FRect = self.image.get_frect()

        self.X = 0
        self.Y = 0
        self.rect.center = (self.X + (self.WIDTH//2), -self.Y + (self.HEIGHT//2))
        

        self.Mass = mass
        
        self.VelocityX, self.VelocityY = 0, 0
        self.AccelerationX, self.AccelerationY = 0, 0

        self.isStationary = stationary

        self.orbitLine = []

    def update(self, planets : pygame.sprite.Group):

        totalAccelX = totalAccelY = 0
        if not self.isStationary:
            for planet in planets:
                if self == planet:
                        continue
                ax, ay = self.attraction(body = planet)
                totalAccelX += ax
                totalAccelY += ay
            
            self.VelocityX += -(totalAccelX)
            self.VelocityY += -(totalAccelY)# * self.TIMESTEP)
            
            self.X += self.VelocityX
            self.Y += self.VelocityY
        else:
             self.VelocityX = self.VelocityY = 0
    

        self.rect.center = (self.X + (self.WIDTH//2), -self.Y + (self.HEIGHT//2))


    def attraction(self, body):
        angle= atan2(self.Y,self.X)
        distance = sqrt((body.X - self.X)**2 + (body.Y - self.Y)**2)

        #gravitational accel
        accel = body.Mass/(distance**2)

        accelX = cos(angle) * accel
        accelY = sin(angle) * accel

        return accelX, accelY
    
    # TODO generates an orbit from parameters
    def set_orbit(self, body, initialAnomaly : float, apoapsis : float, periapsis : float):

        # semi-major and semi-minor axes
        semiMajorAxis = (apoapsis + periapsis) / 2
        semiMinorAxis = sqrt(apoapsis * periapsis)
        # eccentricity
        eccentricity = sqrt(1 - (semiMinorAxis**2/semiMajorAxis**2))

        # TODO: determine orbital position
        r = semiMajorAxis * ((1 - eccentricity**2)/ (1 + eccentricity*cos(radians(initialAnomaly))))
        
        # at initial (true) anomaly of 0, object is at periapsis (on the +x-axis)
        self.X = r*cos(radians(initialAnomaly))
        self.Y = r*sin(radians(initialAnomaly))

        # determine velocity
        velocity = sqrt(body.Mass/ r) # TODO implement the constants
        self.VelocityX = velocity*sin(radians(initialAnomaly))
        self.VelocityY = velocity*cos(radians(initialAnomaly))

        
        


    

        
        