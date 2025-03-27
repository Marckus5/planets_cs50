import pygame
import sys

from menu import *
from scene import *

class Simulation():
    TIMESCALE : float = 0.05
    def __init__(self, windowWidth : int, windowHeight : int):
        pygame.init()
        self.running : bool = True

        self.SCREENSIZE = (windowWidth, windowHeight)
        self.window : pygame.Surface = pygame.display.set_mode(self.SCREENSIZE, flags = pygame.RESIZABLE | pygame.SCALED, vsync=1)
        self.window.fill('Gray')
        pygame.display.set_caption("pygame Test")

        self.selectedPlanet = None
        self.screen = pygame.Surface(self.SCREENSIZE)

        self.clock = pygame.time.Clock()
        # font
        self.defaultFont = pygame.Font(pygame.font.get_default_font())
        

    def run(self):
        self.FPS = 60
        self.DELTATIME : float = 1/self.FPS #TODO implement delta-time
        self.scene = Scene(self, 0)
        self.menu = Menu(self, 0)

        self.selectedPlanet = self.scene.planetSelect

        while self.running:
            self.screen.fill('#a0a0a0')

            # Scene
            self.scene.run()
            # Menu
            self.menu.run()

            pygame.display.update(self.screen)
            self.window.blit(self.screen, (0,0))
            self.check_events()



            self.DELTATIME : float = self.clock.tick(self.FPS)/ (1000)

            pygame.display.set_caption(f"pygame Test | FPS: {self.clock.get_fps():.2f}")

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
            if event.type == pygame.MOUSEWHEEL:
                self.scene.planetList.zoom += event.y * 0.03
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PERIOD:
                    self.TIMESCALE += 0.25
                elif event.key == pygame.K_COMMA:
                    self.TIMESCALE -= 0.25
                


        if self.TIMESCALE < 0.5:
            self.TIMESCALE = 0.5
        elif self.TIMESCALE > 5.0:
            self.TIMESCALE = 4.0
        else:
            self.scene.TIMESTEP = 0.1 * self.DELTATIME * self.TIMESCALE
    
        if self.scene.planetList.zoom < 0.7:
            self.scene.planetList.zoom = 0.7
        elif self.scene.planetList.zoom > 1.5:
            self.scene.planetList.zoom = 1.5

        # CAMERA CONTROLS
        if keys[pygame.K_UP]:
            cameraPos.y += 10 / self.scene.planetList.zoom
        if keys[pygame.K_DOWN]:
            cameraPos.y -= 10 / self.scene.planetList.zoom
        if keys[pygame.K_RIGHT]:
            cameraPos.x -= 10 / self.scene.planetList.zoom
        if keys[pygame.K_LEFT]:
            cameraPos.x += 10 / self.scene.planetList.zoom
        if mButtonsHold[2]:
            cameraPos += mDragPos / self.scene.planetList.zoom
        # TODO CHANGE TIMESCALE
        
        if mButtonsPress[0]:
            # TODO Select Menu
            if self.menu.rect.collidepoint(mPos):
                for button in self.menu.menuList.sprites():
                    offsetButtonPos : pygame.Vector2 = pygame.Vector2(button.rect.topleft) + pygame.Vector2(self.menu.rect.topleft) + pygame.Vector2(self.menu.tabRect.topleft)

                    # TODO menu options
                    if pygame.Rect(offsetButtonPos, button.rect.size).collidepoint(mPos):
                        if button.id == 'test':
                            print("Press: " + button.id)
            # TODO Select Planet
            elif self.scene.rect.collidepoint(mPos):
                for planet in self.scene.planetList.sprites():
                    # BUG: planet rect not consistent with screen when zooming
                    planetOffsetRect : pygame.Rect = planet.rect.copy()
                    planetOffsetRect.topleft += cameraPos
                    planetOffsetRect.scale_by_ip(2)

                    if planetOffsetRect.collidepoint(mPos):
                        self.selectedPlanet.add(planet)
                        break
                    elif self.selectedPlanet:
                        self.selectedPlanet.empty() # Deselect
        
                






