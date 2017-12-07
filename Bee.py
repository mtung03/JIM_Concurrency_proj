#
"""
 Jeremy Su, Ian Mao, Max Tung - Team JIM
 12/7/17
 Comp 50CP

 This module represents the Bee class that the player will control in terms of
 movement. smallgame.py, our UI controller detects arrow-key input and calls
 the appropriate move function of this bee to move its Row, Column and bee_loc
 attributes.
"""
import threading
class Bee(object):
    def __init__(self, Name, Row, Column, MapSize):
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.Points = 0
        self.MapSize = MapSize
        self.bee_loc = (0, 0) # used by Toad
        self.bee_loc_mutex = threading.Lock() # acquired by Toad
 
    def move(self, Direction):
        """Changes the Row, Column and bee_loc of this object according to the
           direction string it receives.
     
        Args:
            Direction: a string of either "UP", "LEFT", "RIGHT" or "DOWN"
  
        Returns:
            Nothing
        """
        if Direction == "UP":
            if self.Row > 0:
                self.Row -= 1
        elif Direction == "LEFT":
            if self.Column > 0:
                self.Column -= 1
        elif Direction == "RIGHT":
            if self.Column < self.MapSize-1:
                self.Column+= 1
        elif Direction == "DOWN":
            if self.Row < self.MapSize-1:
                self.Row += 1
        with self.bee_loc_mutex:
            self.bee_loc = (self.Row, self.Column)
