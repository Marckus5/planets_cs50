import pygame
from math import sin, cos, atan2, sqrt, cos, radians


WHITE = (255,255,255)

class Planet(pygame.sprite.Sprite):
    AU : float = 149.6e9
    G : float = 6.67428e-11
    SCALE : float = 50/AU
    

    def __init__(self, scene, mass : float, color, radius : int, stationary : bool = False):
        super().__init__()
        self.scene = scene
        self.WIDTH, self.HEIGHT = self.scene.simulation.screen.get_size()

        self.TIMESTEP : float = self.scene.simulation.DELTATIME 

        self.Radius = radius
        self.Color = color
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        
        self.rect : pygame.FRect = self.image.get_frect()

        self.X = 0.
        self.Y = 0.
        self.rect.center = (self.X + (self.WIDTH//2), -self.Y + (self.HEIGHT//2))
        

        self.Mass = mass
        
        self.VelocityX, self.VelocityY = 0., 0.
        self.AccelerationX, self.AccelerationY = 0., 0.

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
            
            self.VelocityX += -(totalAccelX * self.TIMESTEP)
            self.VelocityY += -(totalAccelY * self.TIMESTEP)# * self.TIMESTEP)
            
            self.X += self.VelocityX * self.TIMESTEP
            self.Y += self.VelocityY * self.TIMESTEP
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
    

    # generates an orbit using 2-body physics
    # parent: the parent body the object orbits
    # initialAnomaly: the initial (true) anomaly--angle between periapsis and object position
    # periapsisAngle: angle between periapsis position vector and +x-axis
    def set_orbit(self, parent, initialAnomaly : float, apoapsis : float, periapsis : float, periapsisAngle: float = 0):

        massConstant = parent.Mass # TODO implement the gravitation constant

        # semi-major and semi-minor axes
        semiMajorAxis = (apoapsis + periapsis) / 2 #a
        semiMinorAxis = sqrt(apoapsis * periapsis) #b
        # eccentricity
        eccentricity = sqrt(1 - (semiMinorAxis**2/semiMajorAxis**2))

        r = semiMajorAxis * ((1 - eccentricity**2)/ (1 + eccentricity*cos(radians(initialAnomaly))))

        SOI = 0.9431 * semiMajorAxis * (self.Mass/parent.Mass)**(2./5.)
        print(SOI)
          
        # at initial (true) anomaly of 0, object is at periapsis (on the +x-axis)
        self.X = parent.X + r*cos(radians(initialAnomaly + periapsisAngle))
        self.Y = parent.Y + r*sin(radians(initialAnomaly + periapsisAngle))

        # determine velocity using vis-visa equation
        velocity = sqrt(massConstant * ((2/r) - (1/semiMajorAxis)))
        self.VelocityX = parent.VelocityX - velocity*sin(radians(initialAnomaly + periapsisAngle))
        self.VelocityY = parent.VelocityY + velocity*cos(radians(initialAnomaly + periapsisAngle))

        
    # TODO collisions
        


    

        
        