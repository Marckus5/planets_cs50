import pygame


class Menu():
    def __init__(self, simulation : pygame.Surface, tab : int = 0):
        self.simulation = simulation
        self.tab = tab # TODO use for tabs

        self.SIZE: tuple = (self.simulation.SCREENSIZE[0] * 0.25, self.simulation.SCREENSIZE[1])
        self.MARGIN : int = 20

        self.surface = pygame.Surface(self.SIZE).convert()
        self.rect = self.surface.get_rect(topleft = (self.simulation.SCREENSIZE[0]*0.75, 0))
        self.cursorRect = pygame.Rect(0,0,20,20)    

        self.menuList = pygame.sprite.Group()
        test = Button("test","TEST",self.simulation.defaultFont, (self.MARGIN,10))
        self.menuList.add(test)
        test2 = Button("test2","TEST",self.simulation.defaultFont, (self.MARGIN,50))
        self.menuList.add(test2)

        self.index = 0


    def run(self):
        self.surface.fill('grey')

        self.blit_screen()


    def draw_cursor(self):
        
        #cursor location
        if bool(self.menuList):
            pygame.draw.rect(self.surface, 'red', self.menuList[self.index].rect, 2)
        else: 
            pygame.draw.rect(self.surface, 'red', self.cursorRect)

    def blit_screen(self): #NOTE always called last!!!
        
        self.menuList.draw(self.surface)
        
        self.simulation.screen.blit(self.surface, self.rect)

    

class Button(pygame.sprite.Sprite):
    def __init__(self, id : str, text : str, font : pygame.Font, position: tuple = (0,0) , fontColor = "#0f0f0f"):
        super().__init__()
        self.id = id #use for functions
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'red', self.rect, 5)
        self.Position = position
        self.rect.move_ip(self.Position)

