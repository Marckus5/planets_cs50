import pygame


class Menu():
    def __init__(self,display : pygame.Surface, state : int):
        self.display = display
        self.state = state


        self.surface = pygame.Surface(self.game.screenSize).convert()
        self.cursorRect = pygame.Rect(0,0,20,20)

        self.menuList = []

        self.index = 0


    def run(self):
        self.surface.fill('red')

    def draw_cursor(self):
        
        #cursor location
        if bool(self.menuList):
            pygame.draw.rect(self.surface, 'red', self.menuList[self.index].rect, 2)
        else: 
            pygame.draw.rect(self.surface, 'red', self.cursorRect)

    def blit_screen(self): #NOTE always called last!!!
        
        for button in self.menuList:
            button.draw()

        
        self.game.window.blit(self.surface,(0,0))
        pygame.display.flip()

    