'''
Author Prachi (Ana) Kapur

'''

import pygame
import sys
import time

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans.ttf', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
  
            
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2 - 90))
    MenuDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)
    
def redrawWin():
    MenuDisplay.fill(deep_pink)
    playButton.draw(MenuDisplay, black)
    


pygame.init()

display_width = 800
display_height = 600

MenuDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Matching Game')

#colors
white = (255,255,255)
black = (0,0,0)
deep_pink = (255,20,147)
pink = (255,192,203)

playButton = button(pink,(display_width/2 - 100),(display_height/2), 100, 100, 'Play' )

while (True):
    redrawWin()   
    pygame.display.update()
    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            pygame.quit(); 
            sys.exit();
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.isOver(pos):
                print("clicked") #TODO: instead of clicked go to file
                
                
    message_display('Welcome to the Matching Game')
   
    
           
                
            
            
            
            
            
            
            
            
            
            