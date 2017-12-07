#
"""
 Jeremy Su, Ian Mao, Max Tung - Team JIM
 12/7/17
 Comp 50CP

 This module represents the Bird class that will be one of the enemies that
 player has to avoid. The bird randomly chooses a direction and moves there
 if possible. The toad itself is a thread and will change its
 movement every 0.3 seconds. Since this is a separate thread, this class has
 a field StopEvent which is the condition of the whileloop to keep running.
 This can be triggered externally and is called by the gamemanager.
"""

import threading
import random
import time

class Bird(threading.Thread):
    def __init__(self, Name, Row, Column, MapSize):
        threading.Thread.__init__(self)
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.MapSize = MapSize
        self.StopEvent = threading.Event()

    def run(self):
        """Keeps looping until it is told to stop. Finds the location of the Bee
           and goes in the direction it's at with each iteration.
     
        Args:
            Nothing
  
        Returns:
            Nothing
        """
        while not self.stopped():
            Direction = random.randint(0, 3)
            if Direction == 0: # UP
                if self.Row > 0:
                    self.Row -= 1
            elif Direction == 1: # LEFT
                if self.Column > 0:
                    self.Column -= 1
            elif Direction == 2: # RIGHT
                if self.Column < self.MapSize-1:
                    self.Column += 1
            elif Direction == 3: # DOWN
                if self.Row < self.MapSize-1:
                    self.Row += 1
            time.sleep(0.2) # moves every 0.2 seconds

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


