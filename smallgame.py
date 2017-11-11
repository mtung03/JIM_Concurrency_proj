import pygame
import random

pygame.init()
Screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
Done = False
MapSize = 20

TileWidth = 25
TileHeight = 25
TileMargin = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class MapTile(object):
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row

class Map(object):
    Grid = []

    for Row in range(MapSize):     # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     # Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("ground", Column, Row)
            Grid[Column][Row] = TempTile

    for i in range(20):            # Placing random flowers on the map
        randomRow = random.randint(0, MapSize - 1)
        randomCol = random.randint(0, MapSize - 1)
        print ("row: %i, col: %i" %(randomRow, randomCol))
        tile = MapTile("flower", randomRow, randomCol)
        Grid[randomRow][randomCol] = tile

Map = Map()

while not Done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            if Map.Grid[Column][Row].Name == "flower":
                Color = RED
            else:
                Color = WHITE
            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])
    clock.tick(60)
    pygame.display.flip()

pygame.quit()