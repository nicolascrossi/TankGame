import math


class Line:

    def __init__(self, x, y, rise, run):
        self.x1 = x
        self.y1 = y
        self.x2 = x + run
        self.y2 = y + rise

    def dist(self, x, y):
        num = abs((self.x2 - self.x1)*(self.y1 - y) -
                  (self.x1 - x)*(self.y2 - self.y1))
        denom = math.sqrt(((self.x2 - self.x1) ** 2) +
                          ((self.y2 - self.y1) ** 2))
        return num / denom
