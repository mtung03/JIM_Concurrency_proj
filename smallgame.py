import pygame
import random
import threading
from GameManager import GameManager

pygame.init()
Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
Done = False
MapSize = 20

TileWidth = 25
TileHeight = 25
TileMargin = 5

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)

flowerImg = pygame.image.load("flower.png")
flowerImg = pygame.transform.scale(flowerImg, (TileWidth, TileHeight))

beeImg = pygame.image.load("bee.png")
beeImg = pygame.transform.scale(beeImg, (TileWidth, TileHeight))

birdImg = pygame.image.load("bird.png")
birdImg = pygame.transform.scale(birdImg, (TileWidth, TileHeight))

groundImg = pygame.image.load("ground.png")
groundImg = pygame.transform.scale(groundImg, (TileWidth, TileHeight))

Images = {
    "FLOWER" : flowerImg,
    "BEE"    : beeImg,
    "BIRD"   : birdImg,
    "GROUND" : groundImg
}

KeyLookup = {
    pygame.K_LEFT   : "LEFT",
    pygame.K_RIGHT  : "RIGHT",
    pygame.K_DOWN   : "DOWN",
    pygame.K_UP     : "UP"
}

gm = GameManager(MapSize)

while not Done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
        elif event.type == pygame.KEYDOWN:
            gm.Bee.move(KeyLookup[event.key])

    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            # for i in range(len(gm.Grid[Column][Row])):
                # if gm.Grid[Column][Row][i].Name == "FLOWER":
                #     Color = RED
                # elif gm.Grid[Column][Row][i].Name == "BEE":
                #     Color = BLUE
                # elif gm.Grid[Column][Row][i].Name == "":
                #     Color = GREEN
                # else: 
                #     Color = WHITE
            img = Images[gm.Grid[Column][Row][-1].Name]
            # pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
            #                                  (TileMargin + TileHeight) * Row + TileMargin,
            #                                  TileWidth,
            #                                  TileHeight])
            Screen.fill((0, 0, 0), [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])
            Screen.blit(img, ((TileMargin + TileWidth) * Column + TileMargin, (TileMargin + TileHeight) * Row + TileMargin))
    clock.tick(60)
    pygame.display.flip()
    gm.update()

pygame.quit()