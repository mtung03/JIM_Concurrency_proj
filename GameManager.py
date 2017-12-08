#
"""
 Jeremy Su, Ian Mao, Max Tung - Team JIM
 12/7/17
 Comp 50CP

 This module represents the Game Manager that keeps track of all the enemy
 threads, the player Bee object, flower placements, and the grid that each
 thread traverses. The game manager is the class that determines if the
 Bee collides with a Toad or Bird, and if a Bee lands on a flower.
"""
import random
import threading
from Bee import Bee
from Bird import Bird
from Toad import Toad

class MapTile(object):
    """
    Represents a base tile of the grid. The name of this tile should either be
    FLOWER or GROUND
    """
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class GameManager(object):
    """
    The game manager contains fields for its size, its state of whether or not
    the game is won, lost, or running, and a Grid to keep track of everything.
    The grid is a 2D list where each slot contains layers. For example, a flower
    tile can be placed on top of a ground tile, so when a flower is collected,
    the ground tile is still there.
    """
    def __init__(self, size, numBirds, numToads):
        self.size = size
        self.Grid = []
        self.State = 0 # 0 = running, -1 = lost, 1 = won
        for Row in range(size): # Creating grid
            self.Grid.append([])
            for Column in range(size):
                self.Grid[Row].append([])
        
        for Row in range(size):     # Filling grid with ground tiles
            for Column in range(size):
                TempTile = MapTile("GROUND", Column, Row)
                self.Grid[Column][Row].append(TempTile)
        
        for i in range(20):            # Placing random flowers tiles on the map
            randomRow = random.randint(0, size - 1)
            randomCol = random.randint(0, size - 1)
            TempTile = MapTile("FLOWER", randomRow, randomCol)
            self.Grid[randomRow][randomCol].append(TempTile)

        self.Bee = Bee("BEE", size / 2, size / 2, size) # Bee placed in center

        # initialize all enemy threads
        self.Birds = [Bird("BIRD", self.randomSpot(), self.randomSpot(), size) 
                                                    for i in range (numBirds)]
        self.Toads = [Toad("TOAD", self.randomSpot(), self.randomSpot(), size, 
                                          self.Bee) for i in range (numToads)]
        # start all enemy threads
        for bird in self.Birds:
            bird.start()
        for toad in self.Toads:
            toad.start()

    def randomSpot(self):
        """Returns a random position within the bounds of the grid
     
        Args:
            Nothing
  
        Returns:
            A random number between 0 and size of grid
        """
        return random.randint(0, self.size - 1)

    def deleteRow(self, Row):
        """Goes through every column in the given row and removes any moving
           entity
     
        Args:
            Row: row number this thread is in charge of processing
  
        Returns:
            Nothing
        """
        for Column in range(self.size):
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
                    

    def update(self):
        """Goes through the entire grid, removes every Bee, Bird, and Toad,
           and detects collisions such as Bee with Flower, or Bird/Toad with Bee
           then places them back onto the grid
     
        Args:
            Nothing
  
        Returns:
            Nothing
        """

        # launches threads for each row to remove moving entities concurrently
        threads = [threading.Thread(target = self.deleteRow, args = [i]) 
                                              for i in range(self.size)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # evaluate game rules - ex) if a bee is on a flower, remove the flower
        if self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][-1].Name \
                                                                    == "FLOWER":
            self.Grid[int(self.Bee.Column)][int(self.Bee.Row)] = \
                         self.Grid[int(self.Bee.Column)][int(self.Bee.Row)][:-1]
            self.Bee.Points += 1
            if self.Bee.Points >= 20: # wins game
                self.State = 1

        # add everything back onto the grid
        self.Grid[int(self.Bee.Column)][int(self.Bee.Row)].append(self.Bee)
        for bird in self.Birds:
            if self.Grid[int(bird.Column)][int(bird.Row)][-1].Name == "BEE":
                self.State = -1 # lost game
                break;
            self.Grid[int(bird.Column)][int(bird.Row)].append(bird)


        for toad in self.Toads:
            if self.Grid[int(toad.Column)][int(toad.Row)][-1].Name == "BEE":
                self.State = -1 # lost game
                break;
            self.Grid[int(toad.Column)][int(toad.Row)].append(toad)
        
        
  



    def stopThreads(self):
        """Stops every bird/toad threads
     
        Args:
            Nothing
  
        Returns:
            Nothing
        """
        for bird in self.Birds:
            bird.stop()

        for toad in self.Toads:
            toad.stop()



