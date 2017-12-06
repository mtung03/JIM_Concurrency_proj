import threading
class Bee(object):
    def __init__(self, Name, Row, Column, MapSize):
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.Points = 0
        self.MapSize = MapSize
        self.bee_loc = (0, 0)
        self.bee_loc_mutex = threading.Lock()
 
    def move(self, Direction):
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
