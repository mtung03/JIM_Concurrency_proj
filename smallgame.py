import pygame
import sys
import random
import threading
from GameManager import GameManager

Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
MapSize = 20
Screen.fill([255, 255, 255])

Colors = {
    "red"   : (255, 0, 0),
    "black" : (0, 0, 0),
    "white" : (255, 255, 255)
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

def gameOver(msg, color):
    font = pygame.font.Font(None, 40)
    text = font.render(msg, True, color)  
    text_rect = text.get_rect()
    text_x = Screen.get_width() / 2 - text_rect.width / 2
    text_y = Screen.get_height() / 2 - text_rect.height / 2    
    Screen.blit(text, [text_x, text_y])

def gameLoop():
    pygame.init()
    gm = GameManager(MapSize)
    gameExit = False  
    while not gameExit:
        if gm.Lost:
            Screen.fill(Colors["white"])
            gameOver("Game Over", Colors["red"])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                    # if event.key == pygame.K_c:
                    #     gameLoop()
        
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

gameLoop()