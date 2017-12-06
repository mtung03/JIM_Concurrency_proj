import pygame
import sys
import random
import threading
import time
from GameManager import GameManager

Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
MapSize = 20
Screen.fill([255, 255, 255])

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
    "FLOWER" : pygame.transform.scale(pygame.image.load("flower.png"), (TileWidth, TileHeight)),
    "BEE"    : pygame.transform.scale(pygame.image.load("bee.png"), (TileWidth, TileHeight)),
    "BIRD"   : pygame.transform.scale(pygame.image.load("bird.png"), (TileWidth, TileHeight)),
    "GROUND" : pygame.transform.scale(pygame.image.load("ground.png"), (TileWidth, TileHeight)),
    "TOAD" : pygame.transform.scale(pygame.image.load("toad.png"), (TileWidth, TileHeight))
} 
KeyLookup = {
    pygame.K_LEFT   : "LEFT",
    pygame.K_RIGHT  : "RIGHT",
    pygame.K_DOWN   : "DOWN",
    pygame.K_UP     : "UP"
}

def changeScreen(msg, color, offset_x, offset_y, size):
    font = pygame.font.SysFont("headlinea", size)
    text = font.render(msg, True, color)  
    text_rect = text.get_rect()
    text_x = Screen.get_width() / 2 - text_rect.width / 2 + offset_x
    text_y = Screen.get_height() / 2 - text_rect.height / 2  + offset_y  
    Screen.blit(text, [text_x, text_y])

def gameLoop(gm):
    pygame.init()
    gameExit = False  
    while not gameExit: #game lost
        if gm.State == -1:
            Screen.fill(Colors["white"])
            changeScreen("Game Over", Colors["red"], 0, 0, 60)
            changeScreen("Press q to quit, c to try again", Colors["black"], 15, 80, 20)
            pygame.display.update()
            gm.stopThreads()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                    if event.key == pygame.K_c:
                        Screen.fill(Colors["white"])
                        gameLoop(GameManager(MapSize))
        elif gm.State == 1:
            Screen.fill(Colors["white"])
            changeScreen("You Win!", Colors["green"], 0, 0, 60)
            changeScreen("Press q to quit, c to try again", Colors["black"], 15, 80, 20)
            pygame.display.update()
            gm.stopThreads()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                    if event.key == pygame.K_c:
                        Screen.fill(Colors["white"])
                        gameLoop(GameManager(MapSize))
        else: #main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                elif event.type == pygame.KEYDOWN:
                    try:
                        gm.Bee.move(KeyLookup[event.key])
                    except KeyError:
                        continue
            for Row in range(MapSize):           # Drawing grid
                for Column in range(MapSize):
                    img = Images[gm.Grid[Column][Row][-1].Name]
                    Screen.fill(Colors["white"], [(TileMargin + TileWidth) * Column + TileMargin,
                                        (TileMargin + TileHeight) * Row + TileMargin,
                                        TileWidth,
                                        TileHeight])
                    Screen.blit(img, ((TileMargin + TileWidth) * Column + TileMargin, 
                                  (TileMargin + TileHeight) * Row + TileMargin))
            clock.tick(60)
            pygame.display.update()
            gm.update()

    gm.stopThreads()
    pygame.quit()

gameLoop(GameManager(MapSize))
