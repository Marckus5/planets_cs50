import pygame


class Menu():
    def __init__(self, simulation : pygame.Surface, tab : int = 0):
        self.simulation = simulation
        

        self.SIZE: tuple = (self.simulation.SCREENSIZE[0] * 0.25, self.simulation.SCREENSIZE[1])
        self.MARGIN : int = 20

        self.surface = pygame.Surface(self.SIZE).convert()
        self.rect = self.surface.get_rect(topleft = (self.simulation.SCREENSIZE[0]*0.75, 0))

        self.tabSurface = pygame.transform.scale(self.surface, (self.SIZE[0]*0.95, self.SIZE[1]* 0.85))
        self.tabRect = self.tabSurface.get_rect(centerx = self.SIZE[0]//2, centery = self.SIZE[1]//2).move(0,10)

        #Tabs
        self.menuList = pygame.sprite.Group()

        self.tab = tab # TODO use for tabs

        
        self.planetUIList = pygame.sprite.Group()
        self.planetList : pygame.sprite.Group = self.simulation.planetList

        menuFont = self.simulation.defaultFont

        # Actions for View tab
        self.viewList = pygame.sprite.Group(
            Text("Planet List:", menuFont, (self.MARGIN, 20)),
            Button("remove", "Remove Selected", menuFont, (self.MARGIN, self.SIZE[1] * .75)),
            Button("goto", "Go to Selected", menuFont, (self.MARGIN, self.SIZE[1] * .8))
            )

        

        isStationaryText = Text("Stationary", menuFont, (self.MARGIN, 20))
        self.buttonStationary = CheckBox("checkbox_stationary", False, (isStationaryText.rect.right + 20, 20))

        buttonAddPlanet = Button("add", "Add Planet", menuFont, (self.MARGIN, self.SIZE[1] * .75))

        self.addOrbitPlanetList = pygame.sprite.Group(
            isStationaryText, self.buttonStationary,
            Text("Name", menuFont, (self.MARGIN, 60)),
            TextBox("input_name", "e.g. Earth", menuFont, (self.MARGIN, 80), numOnly=False),
            Text("Mass", menuFont, (self.MARGIN, 120)),
            TextBox("input_mass", "e.g. 100", menuFont, (self.MARGIN, 140), numOnly=True),
            Text("Color (RGB): 0 - 255", menuFont, (self.MARGIN, 180)),
            TextBox("input_color_r", "R", menuFont, (self.MARGIN, 200), numOnly=True, wrapLength= 60),
            TextBox("input_color_g", "G", menuFont, (self.MARGIN + 80, 200), numOnly=True, wrapLength= 60),
            TextBox("input_color_b", "B", menuFont, (self.MARGIN + 160, 200), numOnly=True, wrapLength= 60),
            Text("Orbital Parameters", menuFont, (self.MARGIN, 240)),
            Text("Initial Anomaly (degrees)", menuFont, (self.MARGIN, 280)),
            TextBox("input_anomaly", "e.g. 10", menuFont, (self.MARGIN, 300), numOnly=True),
            Text("Apoapsis", menuFont, (self.MARGIN, 340)),
            TextBox("input_apoapsis", "e.g. 10", menuFont, (self.MARGIN, 360), numOnly=True),
            Text("Periapsis", menuFont, (self.MARGIN, 400)),
            TextBox("input_periapsis", "e.g. 10", menuFont, (self.MARGIN, 420), numOnly=True),
            Text("Periapsis Angle", menuFont, (self.MARGIN, 460)),
            TextBox("input_periapsis_angle", "e.g. 10", menuFont, (self.MARGIN, 480), numOnly=True),
            buttonAddPlanet
        )
        self.addStationaryPlanetList = pygame.sprite.Group(
            isStationaryText, self.buttonStationary,
            Text("Name", menuFont, (self.MARGIN, 60)),
            TextBox("input_name", "e.g. Earth", menuFont, (self.MARGIN, 80), numOnly=False),
            Text("Mass", menuFont, (self.MARGIN, 120)),
            TextBox("input_mass", "e.g. 100", menuFont, (self.MARGIN, 140), numOnly=True),
            Text("Color (RGB): 0 - 255", menuFont, (self.MARGIN, 180)),
            TextBox("input_color_r", "R", menuFont, (self.MARGIN, 200), numOnly=True, wrapLength= 60),
            TextBox("input_color_g", "G", menuFont, (self.MARGIN + 80, 200), numOnly=True, wrapLength= 60),
            TextBox("input_color_b", "B", menuFont, (self.MARGIN + 160, 200), numOnly=True, wrapLength= 60),
            Text("Position", menuFont, (self.MARGIN, 240)),
            Text("X-Value", menuFont, (self.MARGIN, 260)), TextBox("input_x", "e.g. 10", menuFont, (self.MARGIN + 80, 260), numOnly=True),
            Text("Y-Value", menuFont, (self.MARGIN, 290)), TextBox("input_y", "e.g. 10", menuFont, (self.MARGIN + 80, 280), numOnly=True),
            buttonAddPlanet
        )



        view = Button("tab_view","View", menuFont, (self.MARGIN,10))
        add = Button("tab_add","Add", menuFont, (self.MARGIN + view.rect.right,10))
        self.tabList = pygame.sprite.Group(view, add)

        # timescaling
        slow = Button("slow","<", menuFont, (self.MARGIN,10))
        fast = Button("fast","<", menuFont, (self.MARGIN,10))

        
        # list of functions for each tab
        # 0: view all existing planet objects; move camera to planet; remove planet
        # 1: add planets
        # 2: 
        #


    def run(self):
        self.surface.fill('#dddddd')
        self.tabSurface.fill('#aaaaaa')

        self.update()
        self.blit_screen()

    def blit_screen(self): #NOTE always called last!!!
        self.tabList.draw(self.surface)
        
        
        if self.tab == 0:
            self.render_planet_list()
            
        elif self.tab == 1:
            self.render_add_planet()
            pass
        self.menuList.draw(self.tabSurface)
        
        self.surface.blit(self.tabSurface, self.tabRect)
        self.simulation.screen.blit(self.surface, self.rect)
    
    def update(self):
        self.render_selected()

    def render_selected(self):
        '''Shows the selected planet object'''

        if self.simulation.selectedPlanet:
            text : pygame.Surface = self.simulation.defaultFont.render(f"Selected: {self.simulation.selectedPlanet.sprite.name}", True, '#0f0f0f')
        else:
            text : pygame.Surface = self.simulation.defaultFont.render("Selected: None", True, '#0f0f0f')
        textRect = text.get_rect(bottomleft = (0, self.SIZE[1]))
        self.surface.blit(text, textRect)

    def render_planet_list(self):
        '''lists all planets'''

        y = 60
        # TODO make it so that this only updates when planetList changes
        self.planetUIList.empty()
        for planet in self.planetList.sprites():
            button = Button("planet_"+planet.name, planet.name, self.simulation.defaultFont, (self.MARGIN,y))
            button.planet = planet
            self.planetUIList.add(
                button
            )
            y += 40

        self.planetUIList.draw(self.tabSurface)
        self.menuList = self.viewList.copy()

            
    def render_add_planet(self):
        self.menuList = self.addStationaryPlanetList.copy() if self.buttonStationary.enabled else self.addOrbitPlanetList.copy()


        
    

class Button(pygame.sprite.Sprite):
    def __init__(self, id : str, text : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f"):
        super().__init__()
        self.id = id #use for functions
        self.image = font.render(text, True, fontColor, ('#a0a0a0'))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'grey', self.rect, 1)
        self.Position = position
        self.rect.move_ip(self.Position)

class Text(pygame.sprite.Sprite):
    def __init__(self, text : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f"):
        super().__init__()
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        #pygame.draw.rect(self.image, 'red', self.rect, 5)
        self.Position = position
        self.rect.move_ip(self.Position)

class TextBox(pygame.sprite.Sprite):
    def __init__(self, id : str, placeholder : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f", wrapLength = 200, numOnly : bool = False):
        super().__init__()
        self.id = id #use for functions
        self.font = font
        self.fontColor = fontColor
        self.placeholder = placeholder
        self.wrapLength = wrapLength
        self.image = pygame.Surface((self.wrapLength,20))
        self.rect = self.image.get_rect()
        self.image.fill('white')

        self.Position = position
        self.rect.move_ip(self.Position)

        self.textSurface = self.font.render(self.placeholder, True, self.fontColor, 'white', self.wrapLength)
        self.image.blit(self.textSurface, (0, 0, self.wrapLength, 20))

        self.value : str = ''
        self.selected = False
        self.numOnly = numOnly

    def update(self):
        if self.selected:
            self.textSurface = self.font.render(self.value, True, self.fontColor, 'grey', self.wrapLength)
        elif not bool(self.value):
            self.textSurface = self.font.render(self.placeholder, True, self.fontColor, 'white', self.wrapLength)
            #self.image = self.font.render(self.placeholder, True, self.fontColor, 'white', self.wrapLength)
        else:
            self.textSurface = self.font.render(self.value, True, self.fontColor, 'white', self.wrapLength)
            #self.image = self.font.render(self.value, True, self.fontColor, 'white', self.wrapLength)
        textRect = self.textSurface.get_rect()
        self.image.fill("white")
        self.image.blit(self.textSurface, (textRect.left, 0, self.wrapLength, 20))

class CheckBox(pygame.sprite.Sprite):
    def __init__(self, id : str, enabled : bool, position: tuple = (0,0)):
        super().__init__()
        self.id = id #use for functions
        self.image = pygame.Surface((20,20))
        self.rect = pygame.draw.rect(self.image, 'black', ((0,0), (20,20)))
        pygame.draw.rect(self.image, 'white', ((2,2), (16,16)))

        self.Position = position
        self.rect.move_ip(self.Position)

        self.enabled = enabled

    def update(self):
        if self.enabled:
            pygame.draw.rect(self.image, 'red', ((2,2), pygame.Vector2(self.rect.size) * 0.8))
        else:
            pygame.draw.rect(self.image, 'black', ((0,0),self.rect.size))
            pygame.draw.rect(self.image, 'white', ((2,2), pygame.Vector2(self.rect.size) * 0.8))

