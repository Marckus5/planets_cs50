from numpy import *
import pygame
import math

WIDTH, HEIGHT = 800, 800

WHITE = [255,255,255]
BLACK = [0,0,0]
YELLOW = [255,255,0]
BLUE = [0,0,255]
RED = [255,0,0]
BROWN = [150,80,80]
#initialize
pygame.init()

#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit")


def main():

    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()

    #initialize planet
    sun = Planet(mass = 1.98892e30, color = YELLOW, radius = 16, x = -1* Planet.AU, y = 0.* Planet.AU)
    sun.VelocityY = 15e3
    
    earth = Planet(mass = 5.9742e24, color = BLUE, radius = 4,  x = 0.* Planet.AU, y = 4.* Planet.AU)
    earth.VelocityX = 29.783e3
    earth.VelocityX = 20.783e3
    mars = Planet(mass = 6.39e23, color = RED, radius = 4,  x = 4.8* Planet.AU, y = 0 * Planet.AU)
    mars.VelocityY = -24.077e3
    mars.VelocityY = -18.783e3


    sun2 = Planet(mass = 1.98892e30, color = YELLOW, radius = 16, x = 1* Planet.AU, y = 0.* Planet.AU)
    sun2.VelocityY = -15e3

    mercury = Planet(mass = 3.39e23, color = WHITE, radius = 4,  x = 0 * Planet.AU, y = 3 * Planet.AU)
    mercury.VelocityX = 27e3

    jupiter = Planet(mass = 3.39e24, color = BROWN, radius = 8,  x = 8 * Planet.AU, y = 0 * Planet.AU)
    jupiter.VelocityY = -15e3



    planet1 = Planet(mass = 5.9742e24, color = BLUE, radius = 8, x = -7* Planet.AU, y = 3.* Planet.AU)
    planet1.VelocityX = 15e3
    sun1 = Planet(mass = 1.98892e30, color = YELLOW, radius = 32, x = 0. * Planet.AU, y = 0.* Planet.AU)
    #sun2 = Planet(mass = 1.98892e30, color = RED, radius = 32, x = 0 * Planet.AU, y = 2.* Planet.AU)
    #all planets
    planets = [planet1, sun1]
    suns = [sun1]
    
    
    
    pause = True
    while running:

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

        clock.tick(60)
        pygame.display.update()

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = True

        #fill background to black
        screen.fill(BLACK)

        #update position
        #for planet in planets:
        #    planet.update(planets)

        planet1.update(suns)
        #draw trajectory
        for planet in planets:
            planet.draw_orbit(screen)
        # Draw objects
        for planet in planets:
            planet.draw(win=screen)


        

    # Done! Time to quit.
    pygame.quit()


class Planet():
    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 50/AU
    TIMESTEP = 3600 * 24 *10

    def __init__(self, mass, color, radius, x, y):
        self.X = x
        self.Y = y
        self.Mass = mass
        self.Color = color
        self.Radius = radius
        self.VelocityX = 0
        self.VelocityY = 0

        self.orbit = []
        self.isSun = False
        self.distanceToSun = 0 

    def draw(self, win):
        x = self.X * self.SCALE + (WIDTH * .5) 
        y = self.Y * self.SCALE + (HEIGHT * .5)

        pygame.draw.circle(win, self.Color, (x,y), self.Radius)
        
    def draw_orbit(self, win):
        if len(self.orbit) > 2:
            updatedPoints = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + (WIDTH * .5) 
                y = y * self.SCALE + (HEIGHT * .5)
                updatedPoints.append((x,y))
            pygame.draw.lines(win, WHITE, False, updatedPoints, 2)

    def attraction(self, body):
        angle= math.atan2(self.Y,self.X)
        distance = math.sqrt((body.X - self.X)**2 + (body.Y - self.Y)**2)

        #gravitational accel
        accel = self.G*body.Mass/(distance**2)

        accelX = cos(angle) * accel
        accelY = sin(angle) * accel

        return accelX, accelY

    def update(self, planets):

        totalAccelX = totalAccelY = 0

        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(body = planet)
            totalAccelX += fx
            totalAccelY += fy
        
        #vel
        self.VelocityX += -(totalAccelX * self.TIMESTEP)
        self.VelocityY += -(totalAccelY * self.TIMESTEP)

        #pos
        self.X += self.TIMESTEP*self.VelocityX
        self.Y += self.TIMESTEP*self.VelocityY

        self.orbit.append((self.X, self.Y))
        if len(self.orbit) > 4096:
            self.orbit.pop(0)

main()