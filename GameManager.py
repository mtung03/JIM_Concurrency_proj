import random
import threading
from Bee import Bee
from Bird import Bird
from Toad import Toad

class MapTile(object):
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class GameManager(object):
    def __init__(self, size):
        self.size = size
        self.Grid = []
        self.State = 0 #0 = running, -1 = lost, 1 = won
        self.Locks = [[threading.Lock for x in range(size)] for y in range(size)]
        for Row in range(size):     # Creating grid
            self.Grid.append([])
            for Column in range(size):
                self.Grid[Row].append([])
        
        for Row in range(size):     # Filling grid with grass
            for Column in range(size):
                TempTile = MapTile("GROUND", Column, Row)
                self.Grid[Column][Row].append(TempTile)
        
        for i in range(20):            # Placing random flowers on the map
            randomRow = random.randint(0, size - 1)
            randomCol = random.randint(0, size - 1)
        # print ("row: %i, col: %i" %(randomRow, randomCol))
            TempTile = MapTile("FLOWER", randomRow, randomCol)
            self.Grid[randomRow][randomCol].append(TempTile)

        RandomRow = random.randint(0, size - 1)      #Dropping the bee in
        RandomColumn = random.randint(0, size - 1)
     

        self.Bee = Bee("BEE", RandomColumn, RandomRow, size, self.Locks)



        self.Birds = [Bird("BIRD", random.randint(0, size - 1), random.randint(0, size - 1), size) for i in range (4)]
        self.Toads = [Toad("TOAD", random.randint(0, size - 1), random.randint(0, size - 1), size, self.Bee) for i in range (1)]

        for bird in self.Birds:
            bird.start()

        for toad in self.Toads:
            toad.start()


    def update(self):
        for Column in range(self.size):      
            for Row in range(self.size):
                # going through the list in each slot to check
                # if there's any internal conflicts
                i = 0
                while i < len(self.Grid[Column][Row]):
                    if self.Grid[Column][Row][i].Column != Column:
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "BEE":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "BIRD":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "TOAD":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    i += 1
                
        # when the bee pollinates a flower overwrite and add to points
        if self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][-1].Name == "FLOWER":
            self.Grid[int(self.Bee.Column)][int(self.Bee.Row)] = self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][:-1]
            self.Bee.Points += 1
            if self.Bee.Points >= 20:
                self.State = 1
        self.Grid[int(self.Bee.Column)][int(self.Bee.Row)].append(self.Bee)

        # when bird hits bee player lost
        
        #elif self.Grid[int(self.Bird.Column)][int(self.Bird.Row)][-1].Name == "TOAD":
        
  
        # when toad hits flower just overwrite
        

        for bird in self.Birds:
            if self.Grid[int(bird.Column)][int(bird.Row)][-1].Name == "BEE":
                self.State = -1
                break;
            self.Grid[int(bird.Column)][int(bird.Row)].append(bird)


        for toad in self.Toads:
            if self.Grid[int(toad.Column)][int(toad.Row)][-1].Name == "BEE":
                self.State = -1
                break;
            self.Grid[int(toad.Column)][int(toad.Row)].append(toad)
        
        
  



    def stopThreads(self):
        for bird in self.Birds:
            bird.stop()

        for toad in self.Toads:
            toad.stop()



