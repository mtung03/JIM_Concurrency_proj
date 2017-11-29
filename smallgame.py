import pygame
import sys
import random
import threading
from GameManager import GameManager

pygame.init()
Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
MapSize = 20

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

gm = GameManager(MapSize)

while not gm.Lost:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gm.stopBirds()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            try:
                gm.Bee.move(KeyLookup[event.key])
            except KeyError:
                continue
    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            img = Images[gm.Grid[Column][Row][-1].Name]
            Screen.fill((0, 0, 0), [(TileMargin + TileWidth) * Column + TileMargin,
                                    (TileMargin + TileHeight) * Row + TileMargin,
                                    TileWidth,
                                    TileHeight])
            Screen.blit(img, ((TileMargin + TileWidth) * Column + TileMargin, 
                              (TileMargin + TileHeight) * Row + TileMargin))
    clock.tick(60)
    pygame.display.flip()
    gm.update()

gm.stopBirds()
pygame.quit()
