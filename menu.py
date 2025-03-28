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
        view = Button("tab_view","View", self.simulation.defaultFont, (self.MARGIN,10))
        self.planetUIList = pygame.sprite.Group()
        self.planetList : pygame.sprite.Group = self.simulation.planetList

        # Actions for View tab
        self.viewList = pygame.sprite.Group(
            Text("Planet List:", self.simulation.defaultFont, (self.MARGIN, 20)),
            Button("remove", "Remove Selected", self.simulation.defaultFont, (self.MARGIN, self.SIZE[1] * .75)),
            Button("goto", "Go to Selected", self.simulation.defaultFont, (self.MARGIN, self.SIZE[1] * .8))
            )

        add = Button("tab_add","Add", self.simulation.defaultFont, (self.MARGIN + view.rect.right,10))

        self.tabList = pygame.sprite.Group(view, add)

        
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
            self.render_view_list()
        elif self.tab == 1:
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

            
    def render_view_list(self):

        self.menuList = self.viewList.copy()
    

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
        self.id = id #use for functions
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        #pygame.draw.rect(self.image, 'red', self.rect, 5)
        self.Position = position
        self.rect.move_ip(self.Position)

