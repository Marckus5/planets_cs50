import pygame
from math import sin, cos, atan2, sqrt, cos, radians


WHITE = (255,255,255)

class Planet(pygame.sprite.Sprite):
    AU : float = 149.6e9
    G : float = 6.67428e-11
    SCALE : float = 50/AU
    TIMESCALE : float = 1

    def __init__(self, scene, name: str, mass : float, color, radius : int, stationary : bool = False):
        super().__init__()
        self.scene = scene
        self.WIDTH, self.HEIGHT = self.scene.simulation.SCREENSIZE

        self.TIMESTEP : float = self.scene.simulation.DELTATIME * self.TIMESCALE

        self.Radius = radius
        self.Color = color
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.name = name
        
        self.rect : pygame.FRect = self.image.get_frect()
        
        self.Position : pygame.Vector2 = pygame.Vector2(0,0)
        self.Velocity : pygame.Vector2 = pygame.Vector2(0,0)
        self.Acceleration : pygame.Vector2 = pygame.Vector2(0,0)
        self.rect.center = (self.Position.x + (self.WIDTH/2), -self.Position.y + (self.HEIGHT/2))

        self.Mass = mass
        
        self.isStationary = stationary

        self.orbitLine = []
        self.orbitLineLen : int = int(self.TIMESTEP) * 100

    def update(self, planets : pygame.sprite.Group):
        
        
        if self.isStationary:
            self.Velocity = pygame.Vector2(0,0)
            #self.VelocityX = self.VelocityY = 0
        else:
            totalAccel = pygame.Vector2(0,0)
            for planet in planets:
                if self == planet:
                    continue
                a = self.attraction(body = planet)
                totalAccel += a
                #totalAccelX += ax
                #totalAccelY += ay
            

            self.Velocity += totalAccel * self.TIMESTEP
            self.Position += self.Velocity * self.TIMESTEP

            # TODO 
            self.orbitLine.append(self.rect.center)
            if len(self.orbitLine) > 300:
                self.orbitLine.pop(0)

        self.rect.center = (self.Position.x + (self.WIDTH/2), -self.Position.y + (self.HEIGHT/2))
            
            

    


    def attraction(self, body):
        angle= atan2(body.Position.y - self.Position.y, body.Position.x - self.Position.x)
        #angle = radians(pygame.Vector2(1,0).angle_to(self.Position))
        distance = (self.Position - body.Position).length()

        #gravitational accel
        accel = body.Mass/float(distance**2.)

    
        accel = pygame.Vector2(cos(angle) * accel, sin(angle) * accel)

        return accel
    

    # generates an orbit using 2-body physics
    # parent: the parent body the object orbits
    # initialAnomaly: the initial (true) anomaly--angle between periapsis and object position
    # periapsisAngle: angle between periapsis position vector and +x-axis
    def set_orbit(self, parent, initialAnomaly : float, apoapsis : float, periapsis : float, periapsisAngle: float = 0):

        massConstant = parent.Mass # TODO implement the gravitation constant

        # semi-major and semi-minor axes
        semiMajorAxis = (apoapsis + periapsis) / 2. #a
        semiMinorAxis = sqrt(apoapsis * periapsis) #b
        # eccentricity
        eccentricity = sqrt(1 - (semiMinorAxis**2/semiMajorAxis**2))

        r = semiMajorAxis * ((1. - eccentricity**2.)/ (1 + eccentricity*cos(radians(initialAnomaly))))

        SOI = 0.9431 * semiMajorAxis * (self.Mass/parent.Mass)**(2./5.)
        print("Sphere of influence of " + self.name + ": " + str(SOI))
          
        # at initial (true) anomaly of 0, object is at periapsis (on the +x-axis)
        self.Position.x = parent.Position.x + r*cos(radians(initialAnomaly + periapsisAngle))
        self.Position.y = parent.Position.y + r*sin(radians(initialAnomaly + periapsisAngle))

        print(parent.Position.x)

        # determine velocity using vis-visa equation
        velocity = sqrt(massConstant * ((2./r) - (1./semiMajorAxis)))
        self.Velocity.x = parent.Velocity.x - velocity*sin(radians(initialAnomaly + periapsisAngle)) #+ velocity*cos(radians(initialAnomaly + periapsisAngle))
        self.Velocity.y = parent.Velocity.y + velocity*cos(radians(initialAnomaly + periapsisAngle)) #+ velocity*sin(radians(initialAnomaly + periapsisAngle))
        
        self.rect.center = (self.Position.x + (self.WIDTH/2), -self.Position.y + (self.HEIGHT/2))
        self.orbitLine = [self.rect.center]

        
    # TODO collisions
        


    

        
        