from multiprocessing import Lock
import random


class Cell(object):
    """A single cell"""
    def __init__(self, position=(0.5, 0.5, 0.5), radius=10.0, cell_types=[]):
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
        random_position=(random.random(), random.random(), random.random())
        child_cell = Cell(position=random_position, radius=self.radius)
        return child_cell
