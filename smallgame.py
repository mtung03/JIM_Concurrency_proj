#
"""
 Jeremy Su, Ian Mao, Max Tung - Team JIM
 12/7/17
 Comp 50CP
 
 This module contains a game manager and runs and displays the main game by
 using the pygame library. 

 In this game, the player controls a Bee and must
 collect all 20 flowers while avoiding Birds and Toads. The Birds and Toads
 are controlled by separate threads while the user must use the arrow keys
 to move the Bee.

 To play the game with the default amount 5 birds and 1 toads go to command
 line and enter:

 python smallgame.py

 or to specify number of birds and toads (remember to enter both!), for example
 to play with 10 birds and 3 toads:

 python smallgame.py 10 3

 After a win or loss, you can press 'q' to quit the game or 'c' to start another
 game with the same configuration.
"""

import pygame
import sys
import random
import threading
from GameManager import GameManager

Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock() # helps with keeping track of time
MapSize = 20
Screen.fill([255, 255, 255])
numBirds = 5 # default
numToads = 1 # default
Colors = {
    "red"   : (255, 0, 0),
    "black" : (0, 0, 0),
    "white" : (255, 255, 255),
    "green" : (50, 205, 50)
}

TileWidth = 25
TileHeight = 25
TileMargin = 5

Images = {
    "FLOWER" : pygame.transform.scale(
        pygame.image.load("flower.png"), (TileWidth, TileHeight)),
    "BEE"    : pygame.transform.scale(
        pygame.image.load("bee.png"), (TileWidth, TileHeight)),
    "BIRD"   : pygame.transform.scale(
        pygame.image.load("bird.png"), (TileWidth, TileHeight)),
    "GROUND" : pygame.transform.scale(
        pygame.image.load("ground.png"), (TileWidth, TileHeight)),
    "TOAD"   : pygame.transform.scale(
        pygame.image.load("toad.png"), (TileWidth, TileHeight))
} 

KeyLookup = {
    pygame.K_LEFT   : "LEFT",
    pygame.K_RIGHT  : "RIGHT",
    pygame.K_DOWN   : "DOWN",
    pygame.K_UP     : "UP"
}

def changeScreen(msg, color, offset_x, offset_y, size):
    """Displays a word on the screen with the specified color and offsets
     
    Args:
        msg:        String to display
        color:      RGB tuple to display in
        offset_x:   horizontal offset from the center
        offset_y:   vertical offset from the center
        size:       size of the grid
  
    Returns:
        Nothing
    """
    font = pygame.font.SysFont("headlinea", size) # default font
    text = font.render(msg, True, color)  
    text_rect = text.get_rect()
    text_x = Screen.get_width() / 2 - text_rect.width / 2 + offset_x
    text_y = Screen.get_height() / 2 - text_rect.height / 2  + offset_y  
    Screen.blit(text, [text_x, text_y])

def gameLoop(gm):
    """Main game loop of the game that takes parses user input, displays
       updates and steps the game.
     
    Args:
        gm: the game manager object of the current game
  
    Returns:
        Nothing
    """
    pygame.init()
    gameExit = False  
    while not gameExit: 
        if gm.State == -1: # game lost
            Screen.fill(Colors["white"])

            # display Game Over
            changeScreen("Game Over", Colors["red"], 0, -20, 60)
            changeScreen("Press q to quit, c to try again", 
                                Colors["black"], 15, 60, 20)
            num_points = str(gm.Bee.Points)
            changeScreen("You collected " + num_points + " flowers!", 
                                Colors["black"], 0, 70, 22)
            pygame.display.update()
            gm.stopThreads()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit the game
                        gameExit = True
                    if event.key == pygame.K_c: # play another game
                        Screen.fill(Colors["white"])
                        gameLoop(GameManager(MapSize, numBirds, numToads))
        elif gm.State == 1: # game won
            Screen.fill(Colors["white"])

            # display You Win!
            changeScreen("You Win!", Colors["green"], 0, -20, 60)
            changeScreen("Press q to quit, c to try again", 
                                Colors["black"], 15, 60, 20)
            pygame.display.update()
            gm.stopThreads()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit the game
                        gameExit = True
                    if event.key == pygame.K_c: # play another game
                        Screen.fill(Colors["white"])
                        gameLoop(GameManager(MapSize, numBirds, numToads))
        else: # main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # exiting the window
                    gameExit = True
                elif event.type == pygame.KEYDOWN:
                    try:
                        gm.Bee.move(KeyLookup[event.key]) # move the bee
                    except KeyError:
                        continue
            for Row in range(MapSize):           # Drawing grid
                for Column in range(MapSize):
                    img = Images[gm.Grid[Column][Row][-1].Name]
                    Screen.fill(Colors["white"], 
                                [(TileMargin + TileWidth) * Column + TileMargin,
                                   (TileMargin + TileHeight) * Row + TileMargin,
                                                         TileWidth, TileHeight])
                    Screen.blit(img, 
                                ((TileMargin + TileWidth) * Column + TileMargin, 
                                  (TileMargin + TileHeight) * Row + TileMargin))
            clock.tick(60) # frames per second
            pygame.display.update() # update the display
            gm.update() # update the game manager

    gm.stopThreads()
    pygame.quit()

def main(args):
    """Initiailizes the game manager and uses the default or user-input from
       stdin to change number of toads or birds
     
    Args:
        args: arguments from stdin
  
    Returns:
        Nothing
    """
    global numBirds, numToads
    if len(args) > 2:
        numBirds = int(args[1])
        numToads = int(args[2])
    gameLoop(GameManager(MapSize, numBirds, numToads))

if __name__ == '__main__':
    main(sys.argv)




