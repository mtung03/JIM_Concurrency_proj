import pygame

pygame.init()
Screen = pygame.display.set_mode([650, 650])
clock = pygame.time.Clock()
Done = False
MapSize = 50

TileWidth = 20
TileHeight = 20
TileMargin = 4

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

    for Row in range(MapSize):     #Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("Grass", Column, Row)
            Grid[Column][Row].append(TempTile)

Map = Map()

while not Done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            for i in range(0, len(Map.Grid[Column][Row])):
                Color = WHITE
            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])
    clock.tick(60)
    pygame.display.flip()

pygame.quit()