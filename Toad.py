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
            time.sleep(0.5)

    def get_direction(self):
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
        self.StopEvent.set()

    def stopped(self):
        return self.StopEvent.isSet()

    
