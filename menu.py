import pygame


class Menu():
    def __init__(self,simulation : pygame.Surface, state : int):
        self.simulation = simulation
        self.state = state # TODO use for tabs

        self.SIZE: tuple = (self.simulation.SCREENSIZE[0] * 0.25, self.simulation.SCREENSIZE[1])
        self.surface = pygame.Surface(self.simulation.SCREENSIZE).convert()
        self.cursorRect = pygame.Rect(0,0,20,20)

        self.menuList = []

        self.index = 0


    def run(self):
        self.surface.fill('blue')

        self.blit_screen()


    def draw_cursor(self):
        
        #cursor location
        if bool(self.menuList):
            pygame.draw.rect(self.surface, 'red', self.menuList[self.index].rect, 2)
        else: 
            pygame.draw.rect(self.surface, 'red', self.cursorRect)

    def blit_screen(self): #NOTE always called last!!!
        
        for button in self.menuList:
            button.draw()

        self.simulation.screen.blit(self.surface, (self.simulation.SCREENSIZE[0]*0.75,0))

    