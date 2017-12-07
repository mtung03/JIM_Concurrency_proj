#
"""
 Jeremy Su, Ian Mao, Max Tung - Team JIM
 12/7/17
 Comp 50CP

 This module represents the Toad class that will be one of the enemies that
 player has to avoid. The toad constantly seeks out the Bee, chasing it around
 but is slower than a bird. The toad itself is a thread and will change its
 movement every 0.5 seconds. Since this is a separate thread, this class has
 a field StopEvent which is the condition of the whileloop to keep running.
 This can be triggered externally and is called by the gamemanager.
"""

import threading
import random
import time

class Toad(threading.Thread):
    def __init__(self, Name, Row, Column, MapSize, Bee):
        threading.Thread.__init__(self)
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.MapSize = MapSize
        self.StopEvent = threading.Event()
        self.Bee = Bee

    def run(self):
        """Keeps looping until it is told to stop. Finds the location of the Bee
           and goes in the direction it's at with each iteration.
     
        Args:
            Nothing
  
        Returns:
            Nothing
        """
        while not self.stopped():
            Direction = self.get_direction()
            if Direction[0] == -1: # UP
                if self.Row > 0:
                    self.Row -= 1
            elif Direction[0] == 1: # DOWN
                if self.Row < self.MapSize-1:
                    self.Row += 1
            if Direction[1] == -1: # LEFT
                if self.Column > 0:
                    self.Column -= 1
            elif Direction[1] == 1: # RIGHT
                if self.Column < self.MapSize-1:
                    self.Column += 1
            time.sleep(0.5) # moves every 0.5 second

    def get_direction(self):
        """Returns a list of an X and Y coordinate which are calculated based on
           the Bee's position and this object's position. Having a list of both
           X and Y allows for diagonal traversal in the grid.
     
        Args:
            Nothing
  
        Returns:
            A list of an X and Y to move: -1 to move left or down, 1 to move right
            or up, and 0 to not move on that dimension.
        """
        with self.Bee.bee_loc_mutex:
            loc = self.Bee.bee_loc
        direction = [0, 0]
        for i in range(4):
            if loc[0] < self.Row:
                direction[0] = -1
            elif loc[0] > self.Row:
                direction[0] = 1
            if loc[1] < self.Column:
                direction[1] = -1
            elif loc[1] > self.Column:
                direction[1] = 1     
        return direction

    def stop(self):
        """Signals the event that this thread is looping on to stop.
     
        Args:
            Nothing
  
        Returns:
            Nothing
        """
        self.StopEvent.set()


    def stopped(self):
        """Checks to see if the event is signaled or not

        Args:
            Nothing
  
        Returns:
            True if the event is signaled, false if it is not
        """
        return self.StopEvent.isSet()


