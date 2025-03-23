import pygame
import sys

from menu import *
from scene import *

class Simulation():
    def __init__(self, windowWidth : int, windowHeight : int):
        pygame.init()
        self.running : bool = True

        self.SCREENSIZE = (windowWidth, windowHeight)
        self.window : pygame.Surface = pygame.display.set_mode(self.SCREENSIZE, flags = pygame.RESIZABLE | pygame.SCALED, vsync=1)
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
        self.DELTATIME : float = 1/self.FPS #TODO implement delta-time
        self.scene = Scene(self, 0)
        while self.running:
            

            self.check_events()
            
            self.scene.run()

            self.window.blit(self.screen, (0,0))
            pygame.display.flip()
            self.DELTATIME : float = self.clock.tick(self.FPS)/ (1000)

        pygame.quit()
        sys.exit()
    

    def check_events(self):
        mPos = pygame.mouse.get_pos()
        mDragPos = pygame.mouse.get_rel()

        mButtonsHold = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        
        cameraPos = self.scene.cameraGroup.Pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
        # TODO CAMERA CONTROLS
        if keys[pygame.K_UP]:
            cameraPos.y += 10
        if keys[pygame.K_DOWN]:
            cameraPos.y -= 10
        if keys[pygame.K_RIGHT]:
            cameraPos.x -= 10   
        if keys[pygame.K_LEFT]:
            cameraPos.x += 10
        
        elif mButtonsHold[2]:
            cameraPos += mDragPos

        
                






