import threading
import random
import time

class Bird(object):
    def __init__(self, Name, Row, Column, MapSize):
        self.Name = Name
        self.Row = Row
        self.Column = Column
        self.Points = 0
        self.MapSize = MapSize
        self.thread = threading.Thread(target = moveBird, args = [self])

def moveBird(Bird):
    while(True):
        Direction = random.randint(0, 4)
        if Direction == 0: # UP
            if Bird.Row > 0:
                Bird.Row -= 1
        elif Direction == 1: # LEFT
            if Bird.Column > 0:
                Bird.Column -= 1
        elif Direction == 2: # RIGHT
            if Bird.Column < Bird.MapSize-1:
                Bird.Column+= 1
        elif Direction == 3: # DOWN
            if Bird.Row < Bird.MapSize-1:
                Bird.Row += 1
        time.sleep(0.5)