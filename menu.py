import pygame


class Menu():
    def __init__(self, simulation : pygame.Surface, tab : int = 0):
        self.simulation = simulation
        self.tab = tab # TODO use for tabs

        self.SIZE: tuple = (self.simulation.SCREENSIZE[0] * 0.25, self.simulation.SCREENSIZE[1])
        self.MARGIN : int = 20

        self.surface = pygame.Surface(self.SIZE).convert()
        self.rect = self.surface.get_rect(topleft = (self.simulation.SCREENSIZE[0]*0.75, 0))

        self.tabSurface = pygame.transform.scale(self.surface, (self.SIZE[0]*0.95, self.SIZE[1]* 0.85))
        self.tabRect = self.tabSurface.get_rect(centerx = self.SIZE[0]//2, centery = self.SIZE[1]//2).move(0,10)

        self.cursorRect = pygame.Rect(0,0,20,20)    

        self.menuList = pygame.sprite.Group()
        test = Button("test","TEST", self.simulation.defaultFont, (self.MARGIN,10))
        self.menuList.add(test)
        test2 = Button("test2","TEST", self.simulation.defaultFont, (self.MARGIN,50))
        self.menuList.add(test2)

        self.index = 0

        # list of functions for each tab
        # 0: view all existing planet objects; move camera to planet
        # 1: add planets
        # 2: 
        #


    def run(self):
        self.surface.fill('#dddddd')
        self.tabSurface.fill('#aaaaaa')

        self.update()
        

        self.blit_screen()

    def blit_screen(self): #NOTE always called last!!!
        
        self.menuList.draw(self.tabSurface)
        
        self.surface.blit(self.tabSurface, self.tabRect)
        self.simulation.screen.blit(self.surface, self.rect)
    
    def update(self):
        self.render_selected()

    def render_selected(self):
        '''Shows the selected planet object'''

        if self.simulation.selectedPlanet:
            text : pygame.Surface = self.simulation.defaultFont.render(f"Selected: {self.simulation.selectedPlanet.sprite.name}", True, '#0f0f0f')
            textRect = text.get_rect(bottomleft = (0, self.SIZE[1]))
        else:
            text : pygame.Surface = self.simulation.defaultFont.render("Selected: None", True, '#0f0f0f')
            textRect = text.get_rect(bottomleft = (0, self.SIZE[1]))
        self.surface.blit(text, textRect)


    

class Button(pygame.sprite.Sprite):
    def __init__(self, id : str, text : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f"):
        super().__init__()
        self.id = id #use for functions
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'red', self.rect, 5)
        self.Position = position
        self.rect.move_ip(self.Position)

class Text(pygame.sprite.Sprite):
    def __init__(self, text : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f"):
        super().__init__()
        self.id = id #use for functions
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'red', self.rect, 5)
        self.Position = position
        self.rect.move_ip(self.Position)

