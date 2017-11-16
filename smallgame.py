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

KeyLookup = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_DOWN: "DOWN",
    pygame.K_UP: "UP"
}

class MapTile(object):
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row

class Bee(object):
    def __init__(self, Name, Row, Column):
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.Points = 0

    def move(self, Direction):
        if Direction == "UP":
            if self.Row > 0:
                self.Row -= 1
        elif Direction == "LEFT":
            if self.Column > 0:
                self.Column -= 1
        elif Direction == "RIGHT":
            if self.Column < MapSize-1:
                self.Column+= 1
        elif Direction == "DOWN":
            if self.Row < MapSize-1:
                self.Row += 1
        Map.update()

class Map(object):
    Grid = []

    for Row in range(MapSize):     # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     # Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("ground", Column, Row)
            Grid[Column][Row].append(TempTile)

    for i in range(20):            # Placing random flowers on the map
        randomRow = random.randint(0, MapSize - 1)
        randomCol = random.randint(0, MapSize - 1)
        # print ("row: %i, col: %i" %(randomRow, randomCol))
        TempTile = MapTile("flower", randomRow, randomCol)
        Grid[randomRow][randomCol].append(TempTile)

    RandomRow = random.randint(0, MapSize - 1)      #Dropping the bee in
    RandomColumn = random.randint(0, MapSize - 1)
    Bee = Bee("Bee", RandomColumn, RandomRow)

    def update(self):
        for Column in range(MapSize):      
            for Row in range(MapSize):
                # going through the list in each slot to check
                # if there's any internal conflicts
                for i in range(len(Map.Grid[Column][Row])):
                    if Map.Grid[Column][Row][i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Bee":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
        # when the bee pollinates a flower
        if Map.Grid[int(Map.Bee.Column)][int(Map.Bee.Row)][-1].Name == "flower":
            Map.Grid[int(Map.Bee.Column)][int(Map.Bee.Row)] = Map.Grid[int(Map.Bee.Column)][int(Map.Bee.Row)][:-1]
            Map.Bee.Points += 1
            print Map.Bee.Points
        Map.Grid[int(Map.Bee.Column)][int(Map.Bee.Row)].append(Map.Bee)


Map = Map()

while not Done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
        elif event.type == pygame.KEYDOWN:
            Map.Bee.move(KeyLookup[event.key])

    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            for i in range(len(Map.Grid[Column][Row])):
                if Map.Grid[Column][Row][i].Name == "flower":
                    Color = RED
                elif Map.Grid[Column][Row][i].Name == "Bee":
                    Color = BLUE
                else: 
                    Color = WHITE
            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])
    clock.tick(60)
    pygame.display.flip()
    Map.update()

pygame.quit()