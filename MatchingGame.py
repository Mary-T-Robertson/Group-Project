import random, pygame, sys
from pygame.locals import *

WINDOW_HEIGHT = 480 # game window height in pixels
WINDOW_WIDTH = 480 # game window width in pixels
BOARD_ROW_COUNT = 4 # number of icon rows
BOARD_COL_COUNT = 4 # number of icon columns
BOX_SIZE = 50 # side length size of (square) icon boxes in pixels
BOX_PADDING = 12 # width of padding between boxes in pixels
HORIZONTAL_MARGIN = int((WINDOW_WIDTH - (BOARD_COL_COUNT * (BOX_SIZE + BOX_PADDING))) / 2) # horizontal distance between game board edge and window edge
VERTICAL_MARGIN = int((WINDOW_HEIGHT - (BOARD_ROW_COUNT * (BOX_SIZE + BOX_PADDING))) / 2) # vertical distance between game board edge and window edge
FRAMES_PER_SECOND = 60 # speed of the program

CLOCK = pygame.time.Clock() # used to manage the framerate of the game (limit game display updates to x number of updates per second)
SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # the display on which we draw our game

# RGB color definitions of various colors we'll use
BACKGROUND_COLOR = (27, 160, 153)
BOX_COLOR = (13, 81, 78)
COLOR_GREEN = (  0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)

# constants we use to refer to different shapes in our game
CIRCLE = 'CIRCLE'
DIAMOND = 'DIAMOND'
OVAL = 'OVAL'
SQUARE = 'SQUARE'

# list of colors to be used in icon creation
ICON_COLORS = (COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_YELLOW)

# list of shapes to be used in icon creation
ICON_SHAPES = (CIRCLE, DIAMOND, OVAL, SQUARE)

# texts displayed in our application
INSTRUCTION_TEXT = "Find all the matching pairs to win."
WIN_TEXT = "You win!!!! Restarting game in 5 seconds..."

def run():
    pygame.event.clear() # workaround to clear event queue to prevent click event from bleeding over from menu program
    pygame.init() # framework call, initialize all imported pygame modules
    pygame.display.set_caption('Simple Matching Game') # set the caption of our display window

    gameBoard = generateRandomGameBoard() # generate our initial game board
    revealedBoxes = generateGridState(False) # generate a list representing all match boxes as "unrevealed"

    # we'll use these variables to store cursor coordinates received from mouse events
    cursorX = 0
    cursorY = 0

    firstSelection = None # stores the (col, row) position of the first box selected

    while True: # main game loop
        mouseClicked = False # used for mouse events
        drawBoard(gameBoard, revealedBoxes) # redraw the game board with current revealed states for all boxes

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): # provide user ability to exit game gracefully
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP: # detect whether user has clicked, if so update click event variables for use below
                cursorX, cursorY = event.pos
                mouseClicked = True

        col, row = findBoxAtCoordinates(cursorX, cursorY) # try to find box at coordinates of mouse click (if one exists at the location of mouse click)
        if col == None or row == None: # couldn't find a box at cursor coordinates from click event (no box clicked)
        	continue # no box was clicked, nothing to update, start again at the top of while-loop

        if not revealedBoxes[col][row] and mouseClicked: # a box was clicked that is not already revealed
            revealedBoxes[col][row] = True # reveal the box
            drawBoard(gameBoard, revealedBoxes) # redraw the board because a box revealed state changed
            if firstSelection == None: # box is first to be selected (resets after second box is selected)
                firstSelection = (col, row) # store the first box clicked so it can be compared to the second box clicked to check for match
            else: # box is second to be selected
                shape1, color1 = getShapeAndColor(gameBoard, firstSelection[0], firstSelection[1]) # get the shape and color of the first box that was clicked
                shape2, color2 = getShapeAndColor(gameBoard, col, row) # get the shape and color of the second (current) box that was clicked

                # Check for box icon match
                if shape1 != shape2 or color1 != color2:
                    # Icons don't match (shape and or color). Reset revealed state of both boxes after a brief pause (to allow user to see second box icon)
                    pygame.time.wait(500)
                    revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                    revealedBoxes[col][row] = False
                    drawBoard(gameBoard, revealedBoxes) # redraw the board because a box revealed state changed
                elif gameIsWon(revealedBoxes): # check if game has been won
                    drawBoard(gameBoard, revealedBoxes, WIN_TEXT) # redraw board with win text (pass optional text parameter that says "You win!" to our drawBoard method)
                    pygame.time.wait(5000) # wait 5 seconds to allow user to see WIN_TEXT

                    gameBoard = generateRandomGameBoard() # Reset the game board (generate and shuffle new icons/boxes)
                    revealedBoxes = generateGridState(False) # generate a list representing all match boxes as "unrevealed"
                    
                    drawBoard(gameBoard, revealedBoxes) # draw the newly reset game board to restart the game

                firstSelection = None # clear firstSelection variable to reset match pair after second consecutive box clicked

        # Calling pygame.time.Clock.tick(x) will order pygame
        # to render only x number times per second. So if your
        # rendering takes 10 milliseconds, it would normally
        # be rendered 100 times per second but calling
        # pygame.time.Clock.tick(60) will cause rendering only
        # 60 times in a second before pygame automatically calls pygame.time.wait()
        CLOCK.tick(FRAMES_PER_SECOND)

# generates a 2d list of TRUE/FALSE values to represent box revealed states
def generateGridState(val):
    revealedBoxes = []
    for i in range(BOARD_COL_COUNT):
        revealedBoxes.append([val] * BOARD_ROW_COUNT)
    return revealedBoxes

# creates a 2d list representing icons and their location on a game board
def generateRandomGameBoard():
    # Generate a list of every shape and color combo
    icons = []
    for color in ICON_COLORS:
        for shape in ICON_SHAPES:
            icons.append( (shape, color) )

    # randomize the icon order
    random.shuffle(icons)
    # determine how many icons we need
    numberOfUniqueIcons = int(BOARD_COL_COUNT * BOARD_ROW_COUNT / 2)
    # double the icon list so that each icon now has a match
    icons = icons[:numberOfUniqueIcons] * 2
    random.shuffle(icons)

    # Map the list of icons to a 2d game board
    board = []
    for x in range(BOARD_COL_COUNT):
        column = []
        for y in range(BOARD_ROW_COUNT):
            column.append(icons[0])
            del icons[0] # remove icon once it's been used
        board.append(column)
    return board

# get the left,top coordinates of box at given (col,row) address
def getBoxOriginCoordinates(col, row):
    # Convert board coordinates to pixel coordinates
    left = col * (BOX_SIZE + BOX_PADDING) + HORIZONTAL_MARGIN
    top = row * (BOX_SIZE + BOX_PADDING) + VERTICAL_MARGIN
    return (left, top)

# try to find box containing given x,y coordinates, returning box (col,row) address if found
def findBoxAtCoordinates(x, y):
    for row in range(BOARD_ROW_COUNT):
        for col in range(BOARD_COL_COUNT):
            left,top = getBoxOriginCoordinates(col, row)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if boxRect.collidepoint(x, y): #collidepoint tests if a point is inside a rect
                return (col, row)
    return (None, None) # no box was found at given x,y coordinates (no box was clicked)

def drawBoard(board, revealed, text=INSTRUCTION_TEXT):
    SURFACE.fill(BACKGROUND_COLOR) # draw background first, gives us a clean slate
    # loop through 2d list of boxes (game board) and draw each box based on its revealed state
    for col in range(BOARD_COL_COUNT):
        for row in range(BOARD_ROW_COUNT):
            left, top = getBoxOriginCoordinates(col, row)
            if not revealed[col][row]:
                # Draw an unrevealed box
                pygame.draw.rect(SURFACE, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                # Draw a revealed box (icon)
                shape, color = getShapeAndColor(board, col, row)
                drawIcon(shape, color, col, row)
    message_display(text) # draw top margin text
    pygame.display.update() # update the display

def drawIcon(shape, color, col, row):
    quarter = int(BOX_SIZE * 0.25) # shorthand, used in shape calculations below. saves us from writing this out 3 times
    half = int(BOX_SIZE * 0.5) # shorthand, used in shape calculations below. saves us from writing this out 10 times

    # get left,top coordinates of box we're drawing an icon on
    # we will draw the icon relative to this starting position
    left, top = getBoxOriginCoordinates(col, row)

    if shape == CIRCLE:
    	# draw a circle around a point
		# circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle(SURFACE, color, (left + half, top + half), half - 5) # logic for drawing a circle
    elif shape == DIAMOND:
		# draw a shape with any number of sides
		# polygon(Surface, color, pointlist, width=0)
        pygame.draw.polygon(SURFACE, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == SQUARE:
    	# draw a rectangle shape
		# rect(Surface, color, Rect, width=0)
		# we'll somewhat arbitrarily draw this square so that it is 1/4 the size of the containing box
		# simply so it does not take up the entire box
        pygame.draw.rect(SURFACE, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == OVAL:
    	# draw a round shape inside a rectangle
		# ellipse(Surface, color, Rect, width=0)
		# flat-ish ellipse, same width as containing box, 1/4 height
        pygame.draw.ellipse(SURFACE, color, (left, top + quarter, BOX_SIZE, half))

# get the shape and color of the box at given col,row address
def getShapeAndColor(board, col, row):
    return board[col][row][0], board[col][row][1]

def gameIsWon(revealedBoxes):
    # Checks whether all boxes have been revealed - if so game is won, otherwise game continues
    for i in revealedBoxes:
        if False in i:
            return False
    return True

def message_display(text):
	font = pygame.font.Font('freesansbold.ttf',20) # set font family and size
	textSurface = font.render(text, True, COLOR_WHITE) # render text in our font+color
	textRect = textSurface.get_rect() # get rect area of text surface
	textRect.center = ((WINDOW_WIDTH/2),(VERTICAL_MARGIN/2)) # center the text within the margin above our game board
	SURFACE.blit(textSurface, textRect) # draw the text on top of our window

# leave this in to launch MatchingGame.py independently of Menu.py for debugging purposes
if __name__ == '__main__':
    run()