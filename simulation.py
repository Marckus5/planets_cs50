import pygame
import sys
import random

from menu import *
from scene import *


class Simulation():
    TIMESCALE : float = 1
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
        self.selectedPlanet = self.scene.planetSelect
        self.planetList = self.scene.planetList
        self.menu = Menu(self, 0)

        self.UIDict = dict()

        self.followobject = False
        while self.running:
            self.screen.fill('#a0a0a0')

            
            
            # Scene
            self.scene.run()
            # Menu
            self.menu.run()

            self.check_events()

            
            self.window.blit(self.screen, (0,0))
            pygame.display.update(self.screen)



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
            elif event.type == pygame.MOUSEWHEEL:
                self.scene.planetList.zoom += event.y * 0.02
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PERIOD:
                    self.TIMESCALE += 0.25
                elif event.key == pygame.K_COMMA:
                    self.TIMESCALE -= 0.25
            
                # Text input
                for UIElement in self.menu.menuList.sprites():
                    if type(UIElement) == TextBox and UIElement.selected:
                        # restrict to numbers
                        numberonly = (event.key >= pygame.K_0 and event.key <= pygame.K_9) or (event.key >= pygame.K_KP0 and event.key <= pygame.K_KP9)
                        if event.key == pygame.K_BACKSPACE:
                            UIElement.value = UIElement.value[:-1]
                        elif UIElement.numOnly:
                            if numberonly:
                                UIElement.value += event.unicode
                        else:
                            UIElement.value += event.unicode

                        UIElement.update()
                    
                    
        # Timescaling
        if self.TIMESCALE < 0.25:
            self.TIMESCALE = 0.25
        elif self.TIMESCALE > 2.0:
            self.TIMESCALE = 2.0
        else:
            self.scene.TIMESTEP = 0.05 * self.DELTATIME * self.TIMESCALE
        # Zoom out
        if self.scene.planetList.zoom < 0.7:
            self.scene.planetList.zoom = 0.7
        # Zoom in
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
            self.followobject = False


        # Update list of planets
        if self.menu.tab == 0:
            self.planetList = self.scene.planetList.sprites()
        
        if self.selectedPlanet:
            # follow object
            if self.followobject:
                cameraPos.x += -self.selectedPlanet.sprite.Position.x - cameraPos.x
                cameraPos.y += self.selectedPlanet.sprite.Position.y - cameraPos.y

        if mButtonsPress[0]:
            # TODO Menu Options
            if self.menu.rect.collidepoint(mPos):
                for UIElement in self.menu.tabList.sprites():
                    offsetButtonPos : pygame.Vector2 = pygame.Vector2(UIElement.rect.topleft) + pygame.Vector2(self.menu.rect.topleft)
                    if pygame.Rect(offsetButtonPos, UIElement.rect.size).collidepoint(mPos):
                        if UIElement.id == "tab_view":
                            self.menu.tab = 0
                            self.menu.menuList.empty()
                            
                        if UIElement.id == "tab_add":
                            self.menu.tab = 1
                            self.menu.planetUIList.empty()
                            self.menu.menuList.empty()
                for UIElement in self.menu.menuList.sprites():
                    offsetButtonPos : pygame.Vector2 = pygame.Vector2(UIElement.rect.topleft) + pygame.Vector2(self.menu.rect.topleft) + pygame.Vector2(self.menu.tabRect.topleft)
                    rect = pygame.Rect(offsetButtonPos, UIElement.rect.size)
                    collision = rect.collidepoint(mPos)
                    
                    # indexing for saving values
                    if type(UIElement) == TextBox:
                        self.UIDict[UIElement.id] = UIElement.value
                        self.UIDict[UIElement.id + '_numOnly'] = UIElement.numOnly
                    if type(UIElement) == CheckBox:
                        self.UIDict[UIElement.id] = UIElement.enabled

                    
                    if collision:
                        if self.selectedPlanet.sprite and type(UIElement) == Button:
                            if self.menu.tab == 0:
                                if UIElement.id == "remove":
                                    self.scene.planetList.remove(self.selectedPlanet.sprite)
                                    self.selectedPlanet.clear()
                                elif UIElement.id == "goto":
                                    # each component is individually changed due to different conventions
                                    # right for the camera position is negative
                                    cameraPos.x += -self.selectedPlanet.sprite.Position.x - cameraPos.x
                                    cameraPos.y += self.selectedPlanet.sprite.Position.y - cameraPos.y
                                    self.followobject = True

                            if self.menu.tab == 1:
                                if UIElement.id == "add":

                                    for key, element in self.UIDict.items():

                                        # convert to appropriate data types
                                        try:
                                            # TODO differentiate between color (int) and other values (float)
                                            
                                            if element == '' and self.UIDict[key+'_numOnly'] and key != 'input_name':
                                                print(f"Missing Values! {key} Putting random values in range 0-255")
                                                self.UIDict[key] = random.randrange(1, 255)
                                                print(f"{element}")
                                            else:
                                                self.UIDict[key] = float(element)

                                            # for limiting color values to 0-255
                                            if key == 'input_color_r' or key == 'input_color_g' or key == 'input_color_b':
                                                if int(element) > 255:
                                                    self.UIDict[key] = 255
                                                elif int(element) < 0:
                                                    self.UIDict[key] = 0
                                            
                                            
                                            
                                            
                                        # if the element is not a float (i.e. the name)
                                        except ValueError:
                                            
                                            pass

                                    if self.UIDict["input_name"] == '':
                                        print("Invalid Name")
                                        continue

                                    try:
                                        # TODO determine radius from mass
                                        radius = self.UIDict["input_mass"]/10 if self.UIDict["input_mass"]/10 > 4 else 4
                                        if radius > 64:
                                            radius = 64

                                        
                                        if self.UIDict["checkbox_stationary"]:
                                            self.scene.add_planet(self.UIDict["input_name"],
                                                                self.UIDict["input_mass"],
                                                                (self.UIDict["input_color_r"],self.UIDict["input_color_g"],self.UIDict["input_color_b"]),
                                                                radius,
                                                                None, 0, 0, 0, 0, False, True, 
                                                                (self.UIDict["input_x"] + self.selectedPlanet.sprite.Position.x, self.UIDict["input_y"] + self.selectedPlanet.sprite.Position.y)
                                                                )
                                        else:
                                            self.scene.add_planet(self.UIDict["input_name"],
                                                                self.UIDict["input_mass"],
                                                                (self.UIDict["input_color_r"],self.UIDict["input_color_g"],self.UIDict["input_color_b"]),
                                                                radius,
                                                                self.selectedPlanet.sprite, 
                                                                self.UIDict["input_anomaly"], 
                                                                self.UIDict["input_apoapsis"], 
                                                                self.UIDict["input_periapsis"], 
                                                                self.UIDict["input_periapsis_angle"], False
                                                                )
                                    except AttributeError:
                                        # if there is a missing value in the dictionary
                                        print("Whoops! You're missing some values!")
                        else:
                            print("Error: No Planet Selected")
                                    

                        # for the add tab
                        if type(UIElement) == CheckBox:
                            UIElement.enabled = not UIElement.enabled
                            UIElement.update()
                        elif type(UIElement) == TextBox:
                            UIElement.selected = True
                            UIElement.update()

                    # Deselect Any Textbox if you click out of them
                    elif type(UIElement) == TextBox:
                            UIElement.selected = False
                            UIElement.update()
                
                            
                # Select planet from menu
                for UIElement in self.menu.planetUIList.sprites():
                    offsetButtonPos : pygame.Vector2 = pygame.Vector2(UIElement.rect.topleft) + pygame.Vector2(self.menu.rect.topleft) + pygame.Vector2(self.menu.tabRect.topleft)
                    if pygame.Rect(offsetButtonPos, UIElement.rect.size).collidepoint(mPos):                        
                        self.selectedPlanet.add(UIElement.planet)

            # TODO Select Planet from scene
            elif self.scene.rect.collidepoint(mPos):
                for planet in self.scene.planetList.sprites():
                    # BUG innacurate hitbox when zoomed
                    planetOffsetRect : pygame.Rect = planet.rect.copy()
                    
                    planetOffsetRect.scale_by_ip((2 * self.scene.planetList.zoom, 2 * self.scene.planetList.zoom))
                    #planetOffsetRect.top *= self.scene.planetList.zoom
                    #planetOffsetRect.left *= self.scene.planetList.zoom
                    planetOffsetRect.topleft += cameraPos * self.scene.planetList.zoom

                    if planetOffsetRect.collidepoint(mPos):
                        #print(planet.name, cameraPos, planet.Position)
                        self.selectedPlanet.add(planet)
                        break
                    elif self.selectedPlanet:
                        self.selectedPlanet.empty() # Deselect
        




