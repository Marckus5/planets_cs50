import pygame
import sys

from menu import *
from scene import *

class Simulation():
    def __init__(self, windowWidth : int, windowHeight : int):
        pygame.init()
        self.running : bool = True

        self.SCREENSIZE = (windowWidth, windowHeight)
        self.window : pygame.Surface = pygame.display.set_mode(self.SCREENSIZE, flags = pygame.RESIZABLE | pygame.SCALED)
        self.window.fill('Gray')
        pygame.display.set_caption("pygame Test")



        self.screen = pygame.Surface(self.SCREENSIZE)        

        self.clock = pygame.time.Clock()

        # font
        self.fontName = pygame.font.get_default_font()
        
        # TODO states
        # 0: Menu
        # 1: Simulation
        # self.state = 0

    def run(self):
        self.FPS = 60
        self.DELTATIME = 1/self.FPS
        self.scene = Scene(self.screen, 0)
        while self.running:
            self.DELTATIME = self.clock.tick(self.FPS)/ 1000

            self.check_events()

            self.screen.fill((0,0,0))
            
            self.scene.run()

            self.window.blit(self.screen, (0,0))
            pygame.display.flip()
            

        pygame.quit()
        sys.exit()
    

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False





