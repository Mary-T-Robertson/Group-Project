'''
Author Prachi (Ana) Kapur

'''

import MatchingGame #imports for the matching game file

import pygame #imports for all of the other relivant packages. 
import sys #system input package
import time #time package for the computer clock

class button():  #class that creates the button object
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        #x y cordinates of the box
        self.x = x 
        self.y = y
        #hight and width of the box
        self.width = width
        self.height = height
        #text  inside of the box 
        self.text = text

    def draw(self,win,outline=None): 
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '': #text is an optional perameter 
            font = pygame.font.SysFont('comicsans.ttf', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def isOver(self, pos): #checks if the mouse is over the button area 
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True  #returns a bool

def text_objects(text, font): #method for the text 
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text): #displays the the test in the intro screen 
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2 - 90))
    MenuDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def redrawWin(): #method that redraws the screen 
    MenuDisplay.fill(deep_pink)
    playButton.draw(MenuDisplay, black)
    message_display('Welcome to the Matching Game')

pygame.init() #initalization of the pygame


'''

first section of code sets up the basic  screen

'''
display_width = 480
display_height = 480
button_height = 100
button_width = 100
MenuDisplay = pygame.display.set_mode((display_width,display_height))
CLOCK = pygame.time.Clock() #sets up clock 
FRAMES_PER_SECOND = 60
pygame.display.set_caption('Matching Game')

#colors
white = (255,255,255)
black = (0,0,0)
deep_pink = (255,20,147)
pink = (255,192,203)

#play button object
playButton = button(pink,(display_width/2 - button_width/2),(display_height/2 - button_height-2) + 50, button_width, button_height, 'Play' )

while (True): #While loop for the game  
    redrawWin() #redraws the window

    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos() #if the 'x' is pressed  the game will quit
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit();
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if playButton.isOver(pos):
                # clear event queue to prevent mouse click from bleeding into MatchingGame
                pygame.event.clear()
                time.sleep(.5)
                MatchingGame.run() #call matching game 

    pygame.display.update() #updates the screen  
    CLOCK.tick(FRAMES_PER_SECOND) 
    
    
    
    