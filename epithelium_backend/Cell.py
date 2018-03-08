
import random
from math import sin, cos

from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend import CellEventList


class Cell(object):
    """A single cell"""
    def __init__(self,
                 position: tuple = (0, 0, 0),
                 radius: float = 1,
                 photoreceptor_type: PhotoreceptorType = PhotoreceptorType.NOT_RECEPTOR,
                 support_specializations: set = None) -> None:
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: A multiplier of the average cell radius
        :param photoreceptor_type: The cells photoreceptor specialization
        :param support_specializations: Set of the cells non-photoreceptor specializations
        """
        self.position_x = position[0]  # type: float
        self.position_y = position[1]  # type: float
        self.position_z = position[2]  # type: float
        self.radius = radius  # type: float
        self.max_radius = 25  # type: float
        self.growth_rate = 1  # type: float
        self.photoreceptor_type = None
        # self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        if support_specializations is None:
            self.support_specializations = set()  # type: set
        else:
            self.support_specializations = support_specializations  # type: set

        # This is a set of the functions which are passively run on this cell during the
        # Epithelium.update functions.  They are added by furrow events.  All cells at least grow passively.
        self.cell_updaters = {CellEventList.passive_growth}  # type: set

    @staticmethod
    def passive_growth(self):
        """
        If this cell's radius is at least the maximum radius for a cell, then calls spawn_new_cell. Otherwise, it will
        grow by the cell's growth rate.
        :return:
        """
        # Check if cell is large enough to divide
        if self.radius >= self.max_radius:
            return self.divide()
        else:
            # If not large enough, grow the cell a little bit for next time
            self.grow_cell(self.growth_rate)
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
        rand_pos = (self.position_x + self.radius * cos(rand_rad), self.position_y + self.radius * sin(rand_rad), 0)
        child_cell = Cell(position=rand_pos, radius=self.radius / 2.0)
        # Find the adjusted position for the original cell for after the division
        self.position_x = self.position_x - self.radius * cos(rand_rad)
        self.position_y = self.position_y - self.radius * sin(rand_rad)
        self.position_z = 0
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

    def dispatch_updates(self):
        """
        Calls all functions in the cell_updaters function list.
        :return:
        """
        for updater in self.cell_updaters:
            updater(self)
