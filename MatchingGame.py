import random, pygame, sys
from pygame.locals import *

WINDOW_HEIGHT = 480 # game window height in pixels
WINDOW_WIDTH = 480 # game window width in pixels
BOARD_ROW_COUNT = 4 # number of icon rows
BOARD_COL_COUNT = 4 # number of icon columns
BOX_SIZE = 50 # side length size of (square) icon boxes in pixels
BOX_PADDING = 12 # width of padding between boxes in pixels
HORIZONTAL_MARGIN = int((WINDOW_WIDTH - (BOARD_COL_COUNT * (BOX_SIZE + BOX_PADDING))) / 2)
VERTICAL_MARGIN = int((WINDOW_HEIGHT - (BOARD_ROW_COUNT * (BOX_SIZE + BOX_PADDING))) / 2)
FRAMES_PER_SECOND = 60 # speed of the program

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND_COLOR = (27, 160, 153)
BOX_COLOR = (13, 81, 78)

# TODO: define some actual shapes and colors
COLOR_1 = (0,0,0)
COLOR_2 = (0,0,0)
COLOR_3 = (0,0,0)
COLOR_4 = (0,0,0)

SHAPE_1 = ("")
SHAPE_2 = ("")
SHAPE_3 = ("")
SHAPE_4 = ("")

ICON_SHAPES = (SHAPE_1, SHAPE_2, SHAPE_3, SHAPE_4)
ICON_COLORS = (COLOR_1, COLOR_2, COLOR_3, COLOR_4)

def run():
    # clear event queue to prevent mouse click from bleeding over from menu program
    pygame.event.clear()
    pygame.init()
    pygame.display.set_caption('Simple Matching Game')
    gameBoard = generateRandomGameBoard()
    revealedBoxes = generateGridState(False)

    cursorX = 0
    cursorY = 0

    firstSelection = None # stores the (col, row) position of the first box selected

    SURFACE.fill(BACKGROUND_COLOR)
    # TODO: add title here something like "find matching pairs to win!"
    initializeGame(gameBoard)

    while True: # main game loop
        mouseClicked = False
        SURFACE.fill(BACKGROUND_COLOR) # drawing the window
        drawBoard(gameBoard, revealedBoxes) 

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                cursorX, cursorY = event.pos
            elif event.type == MOUSEBUTTONUP:
                cursorX, cursorY = event.pos
                mouseClicked = True

        col, row = findBoxAtCoordinates(cursorX, cursorY)
        if col != None and row != None:
            if not revealedBoxes[col][row] and mouseClicked:
                drawBox(gameBoard, (col, row))
                revealedBoxes[col][row] = True # reveal the box
                if firstSelection == None: # box is first to be selected (resets after second box is selected)
                    firstSelection = (col, row)
                else: # box is second to be selected
                    shape1, color1 = getShapeAndColor(gameBoard, firstSelection[0], firstSelection[1])
                    shape2, color2 = getShapeAndColor(gameBoard, col, row)
                    # Check for match
                    if shape1 != shape2 or color1 != color2:
                        # Icons don't match. Hide both icons after a brief pause
                        pygame.time.wait(500)
                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                        revealedBoxes[col][row] = False
                    elif gameIsWon(revealedBoxes): # check if game has been won
                        pygame.time.wait(2000)
                        # TODO: Make the game say "You Win!"
                        # Reset the game board
                        gameBoard = generateRandomGameBoard()
                        revealedBoxes = generateGridState(False)
                        # restart the game
                        initializeGame(gameBoard)           
                    firstSelection = None # reset firstSelection variable

        # Refresh the game window and wait one tick
        pygame.display.update()
        CLOCK.tick(FRAMES_PER_SECOND)

def generateGridState(val):
    revealedBoxes = []
    for i in range(BOARD_COL_COUNT):
        revealedBoxes.append([val] * BOARD_ROW_COUNT)
    return revealedBoxes

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

    # Create the board grid with icons randomly positioned
    board = []
    for x in range(BOARD_COL_COUNT):
        column = []
        for y in range(BOARD_ROW_COUNT):
            column.append(icons[0])
            del icons[0] # remove icon after using so we don't duplicate
        board.append(column)
    return board

def getBoxOriginCoordinates(col, row):
    # Convert board coordinates to pixel coordinates
    left = col * (BOX_SIZE + BOX_PADDING) + HORIZONTAL_MARGIN
    top = row * (BOX_SIZE + BOX_PADDING) + VERTICAL_MARGIN
    return (left, top)

def findBoxAtCoordinates(x, y):
    for row in range(BOARD_ROW_COUNT):
        for col in range(BOARD_COL_COUNT):
            left,top = getBoxOriginCoordinates(col, row)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if boxRect.collidepoint(x, y): #collidepoint tests if a point is inside a rect
                return (col, row)
    return (None, None)

# TODO: Implement functionality to draw different shapes on top of box located at col,row address specified
def drawIcon(shape, color, col, row):
    return

def getShapeAndColor(board, col, row):
    return board[col][row][0], board[col][row][1]

def drawBox(board, box):
    left, top = getBoxOriginCoordinates(box[0], box[1])
    pygame.draw.rect(SURFACE, BACKGROUND_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
    shape, color = getShapeAndColor(board, box[0], box[1])
    drawIcon(shape, color, box[0], box[1])
    pygame.display.update()
    CLOCK.tick(FRAMES_PER_SECOND)

def drawBoard(board, revealed):
    # Draw all the boxes
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

def initializeGame(board):
    #Draw the game board with all boxes covered
    drawBoard(board, generateGridState(False))

def gameIsWon(revealedBoxes):
    # Checks whether all boxes have been revealed - if so game is won, otherwise game continues
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    run()