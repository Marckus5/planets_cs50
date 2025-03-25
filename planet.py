import pygame
from math import sin, cos, atan2, sqrt, cos, radians, pi


WHITE = (255,255,255)

class Planet(pygame.sprite.Sprite):
    TIMESCALE : float = 0.05
    AU : float = 149.6e9
    G : float = 6.67428e-11
    SCALE : float = 50/AU
    

    def __init__(self, scene, name: str, mass : float, color, radius : int, stationary : bool = False):
        super().__init__()
        self.scene = scene
        self.WIDTH, self.HEIGHT = self.scene.SIZE

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
        self.rect.center = (self.Position.x + (self.WIDTH//2), -self.Position.y + (self.HEIGHT//2))

        self.Mass = mass
        
        self.isStationary = stationary

        self.orbitLine = []
        self.orbitLineLen : int = int(self.TIMESTEP * 10e+5)

    def update(self, planets : pygame.sprite.Group):
        if self.isStationary:
            self.Velocity = pygame.Vector2(0,0)
        else:
            totalAccel = pygame.Vector2(0,0)
            for planet in planets:
                if self == planet:
                    continue
                totalAccel += self.attraction(planet)
            

            self.Velocity += totalAccel * self.TIMESTEP
            self.Position += self.Velocity * self.TIMESTEP

            # TODO 
            self.orbitLine.append(pygame.Vector2(self.rect.center))
            if len(self.orbitLine) > self.orbitLineLen:
                self.orbitLine.pop(0)

        self.rect.center = (self.Position.x + (self.WIDTH//2), -self.Position.y + (self.HEIGHT//2))

    def attraction(self, body):
        angle= atan2(self.Position.y - body.Position.y , self.Position.x - body.Position.x)
        #angle = radians(pygame.Vector2(1,0).angle_to(self.Position))
        distance = (self.Position - body.Position).length()

        #gravitational accel
        accel = -body.Mass/float(distance**2.)

    
        accel = pygame.Vector2(cos(angle) * accel, sin(angle) * accel)

        return accel
    

    # TODO: include open orbits where periapsis < 0
    def set_orbit(self, parent, initialAnomaly : float, apoapsis : float, periapsis : float, periapsisAngle: float = 0, retrograde: bool = False):
        """
        Set planet's velocity for an orbit around a central mass. This assumes self.mass << parent.mass
        
        Parameters:
            - parent: the parent body the object orbits
            - initialAnomaly: the initial (true) anomaly--angle between periapsis and object position. In degrees
            - periapsisAngle: angle between periapsis position vector and +x-axis
        """
        # swapping
        if periapsis > apoapsis:
            tmp = periapsis
            periapsis = apoapsis
            apoapsis = tmp

        trueAnomaly = radians(initialAnomaly)

        massConstant = parent.Mass # TODO implement the gravitation constant

        semiMajorAxis = (apoapsis + periapsis) / 2.
        eccentricity = (apoapsis - periapsis)/(apoapsis + periapsis)

        r = semiMajorAxis * ((1. - eccentricity**2.)/ (1 + eccentricity*cos(trueAnomaly)))

        #SOI = 0.9431 * semiMajorAxis * (self.Mass/parent.Mass)**(2./5.)
        #print("Sphere of influence of " + self.name + ": " + str(SOI))
          
        # at initial (true) anomaly of 0, object is at periapsis
        x = r*cos(trueAnomaly)
        y = r*sin(trueAnomaly)
        position = pygame.Vector2(x, y)
        position.rotate_ip(periapsisAngle)
        self.Position = parent.Position + position


        # determine magnitude of velocity using vis-viva equation
        velocityMagnitude = sqrt(massConstant * ((2./r) - (1./semiMajorAxis)))

        # angle between velocity vector and +x-axis
        # BUG Orbit is still a bit off, but it's probably just due to precision error
        flightPathAngle = -atan2((eccentricity*sin(trueAnomaly)),
                                (1 + eccentricity*cos(trueAnomaly)))
        flightPathAngle += 0.5*pi + trueAnomaly

        velocity = pygame.Vector2(1,0).rotate_rad(flightPathAngle) * velocityMagnitude
        velocity.rotate_ip(periapsisAngle)

        self.Velocity = parent.Velocity + velocity

        if retrograde:
            self.Velocity *= -1

        
        self.rect.center = (self.Position.x + (self.WIDTH/2), -self.Position.y + (self.HEIGHT/2))
        self.orbitLine = [pygame.Vector2(self.rect.center)]

        
    # TODO collisions
        


    

        
        