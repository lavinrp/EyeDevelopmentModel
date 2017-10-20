from multiprocessing import Lock
import random
from math import sin, cos

class Cell(object):
    """A single cell"""
    def __init__(self, position=(0.5, 0.5, 0), radius=10.0, cell_types=[]):
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: The radius of the cell
        :param cell_types: The cells specializations
        """
        self.position = position
        self.radius = radius
        self.cell_types = cell_types
        self.seed = random.seed()

    def divide(self):
        rand_rad = random.uniform(2.0, 4.0)
        if self.radius >= .2:
            rand_pos = (self.position[0] + self.radius*cos(rand_rad), self.position[0] + self.radius*sin(rand_rad), 0)
            child_cell = Cell(position=rand_pos, radius=self.radius/2.0)
            self.position = (self.position[0] + self.radius/2.0, self.position[1], self.position[2])
            self.radius /= 2
            return child_cell
        else:
            self.radius += rand_rad/200
            return None
