import random
import threading
from Bee import Bee
from Bird import Bird

class MapTile(object):
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row

class GameManager(object):
    def __init__(self, size):
        self.size = size
        self.Grid = []
        self.Locks = [[threading.Lock for x in range(size)] for y in range(size)]
        for Row in range(size):     # Creating grid
            self.Grid.append([])
            for Column in range(size):
                self.Grid[Row].append([])

        for Row in range(size):     # Filling grid with grass
            for Column in range(size):
                TempTile = MapTile("ground", Column, Row)
                self.Grid[Column][Row].append(TempTile)

        for i in range(20):            # Placing random flowers on the map
            randomRow = random.randint(0, size - 1)
            randomCol = random.randint(0, size - 1)
        # print ("row: %i, col: %i" %(randomRow, randomCol))
            TempTile = MapTile("flower", randomRow, randomCol)
            self.Grid[randomRow][randomCol].append(TempTile)

        RandomRow = random.randint(0, size - 1)      #Dropping the bee in
        RandomColumn = random.randint(0, size - 1)
        self.Bee = Bee("Bee", RandomColumn, RandomRow, size, self.Locks)
        RandomRow = random.randint(0, size - 1)      #Dropping the bee in
        RandomColumn = random.randint(0, size - 1)
        self.Bird = Bird("Bird", RandomColumn, RandomRow, size)
        self.Bird.thread.start()

    def update(self):
        for Column in range(self.size):      
            for Row in range(self.size):
                # going through the list in each slot to check
                # if there's any internal conflicts
                for i in range(len(self.Grid[Column][Row])):
                    if self.Grid[Column][Row][i].Column != Column:
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "Bee":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "Bird":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
        # when the bee pollinates a flower
        if self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][-1].Name == "flower":
            self.Grid[int(self.Bee.Column)][int(self.Bee.Row)] = self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][:-1]
            self.Bee.Points += 1
            print self.Bee.Points
        self.Grid[int(self.Bee.Column)][int(self.Bee.Row)].append(self.Bee)

        if self.Grid[int(self.Bird.Column)][int(self.Bird.Row)][-1].Name == "flower":
            self.Grid[int(self.Bird.Column)][int(self.Bird.Row)] = self.Grid[int(self.Bird.Column)][int(self.Bird.Row)][:-1]
        self.Grid[int(self.Bird.Column)][int(self.Bird.Row)].append(self.Bird)


