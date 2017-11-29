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
        while not self.stopped():
            Direction = random.randint(0, 4)
            if Direction == 0: # UP
                if self.Row > 0:
                    self.Row -= 1
            elif Direction == 1: # LEFT
                if self.Column > 0:
                    self.Column -= 1
            elif Direction == 2: # RIGHT
                if self.Column < self.MapSize-1:
                    self.Column+= 1
            elif Direction == 3: # DOWN
                if self.Row < self.MapSize-1:
                    self.Row += 1
            time.sleep(0.5)

    def stop(self):
        self.StopEvent.set()

    def stopped(self):
        return self.StopEvent.isSet()

    