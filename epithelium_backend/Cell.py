
import random
from math import sin, cos

from epithelium_backend.PhotoreceptorType import PhotoreceptorType


class Cell(object):
    """A single cell"""
    def __init__(self, position=(0.5, 0.5, 0.0), radius=10.0, cell_types=[]):
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: A multiplier of the average cell radius
        :param photoreceptor_type: The cells photoreceptor specialization
        :param support_specializations: Set of the cells non-photoreceptor specializations
        """
        self.position = position  # type: tuple
        self.radius = radius  # type: float
        # self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        # self.support_specializations = support_specializations  # type: set

    def passive_growth(self):
        """
        If this cell's radius is large enough, then calls spawn_new_cell or grown_cell.
        :return:
        """
        # Check if cell is large enough to divide
        if self.radius >= 25:
            return self.spawn_new_cell()
        else:
            # If not large enough, grow the cell a little bit for next time
            self.grow_cell(.01)
            return None

    def divide(self):
        """
        Divides this cell into a new cell with half of this cell's radius.
        Then divides this parent cell's radius in half.
        :return:
        """
        # Choose some radian for direction of placement of new cell
        rand_rad = random.uniform(0, 6.283)
        # Find position for new cell on original cell's circle
        rand_pos = (self.position[0] + self.radius * cos(rand_rad), self.position[0] + self.radius * sin(rand_rad), 0)
        child_cell = Cell(position=rand_pos, radius=self.radius / 2.0)
        # Find the adjusted position for the original cell for after the division
        new_pos = (self.position[0] - self.radius * cos(rand_rad), self.position[0] - self.radius * sin(rand_rad), 0)
        self.position = new_pos
        # Divide the original cell size in half
        self.radius /= 2
        return child_cell

    def grow_cell(self, growth_amount):
        """
        Increases the cell's radius by growth_amount
        :param growth_amount:
        :return:
        """
        self.radius += growth_amount
