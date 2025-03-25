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
            self.screen.fill('#a0a0a0')
            self.scene.run()
            self.window.blit(self.screen, (0,0))
            pygame.display.update(self.screen)

            self.check_events()



            self.DELTATIME : float = self.clock.tick(self.FPS)/ (1000)

        pygame.quit()
        sys.exit()
    

    def check_events(self):
        mPos = pygame.Vector2(pygame.mouse.get_pos())
        mDragPos = pygame.Vector2(pygame.mouse.get_rel())

        mButtonsHold = pygame.mouse.get_pressed()
        mButtonsPress = pygame.mouse.get_just_pressed()
        keys = pygame.key.get_pressed()
        
        cameraPos = self.scene.planetList.Pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # BUG zoom limit is 'bouncy'
            if event.type == pygame.MOUSEWHEEL:
                if self.scene.planetList.zoom < 0.3:
                    self.scene.planetList.zoom = 0.3
                elif self.scene.planetList.zoom > 1.5:
                    self.scene.planetList.zoom = 1.5
                else:
                    self.scene.planetList.zoom -= event.y * 0.03
                print(self.scene.planetList.zoom)
            
        # CAMERA CONTROLS
        if keys[pygame.K_UP]:
            cameraPos.y += 10
        if keys[pygame.K_DOWN]:
            cameraPos.y -= 10
        if keys[pygame.K_RIGHT]:
            cameraPos.x -= 10   
        if keys[pygame.K_LEFT]:
            cameraPos.x += 10
        if mButtonsHold[2]:
            cameraPos += mDragPos
        
        # TODO ZOOM
        zoomTick = 0.01
        if keys[pygame.K_1]:
            if self.scene.zoom > zoomTick:
                self.scene.planetList.zoom -= zoomTick
            else:
                self.scene.planetList.zoom = zoomTick
        if keys[pygame.K_2]:
            self.scene.planetList.zoom += 0.01

        # TODO CHANGE TIMESCALE
        
        if mButtonsPress[0]:
            # TODO Select Planet
            for planet in self.scene.planetList:
                planetOffsetRect : pygame.Rect = planet.rect.copy()
                planetOffsetRect.topleft += cameraPos
                planetOffsetRect.scale_by_ip(2)
                if planetOffsetRect.collidepoint(mPos):
                    print("Selected: " + planet.name)

        
                






