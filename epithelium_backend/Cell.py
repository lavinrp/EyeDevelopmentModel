
import random
from math import sin, cos, sqrt

from epithelium_backend.PhotoreceptorType import PhotoreceptorType


class Cell(object):
    """A single cell"""
    def __init__(self,
                 position: tuple = (0, 0, 0),
                 radius: float = 1,
                 photoreceptor_type: PhotoreceptorType = PhotoreceptorType.NOT_RECEPTOR,
                 support_specializations: set = None,
                 cell_events: set = None) -> None:
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: A multiplier of the average cell radius
        :param photoreceptor_type: The cells photoreceptor specialization
        :param support_specializations: Set of the cells non-photoreceptor specializations
        :param cell_events: Default list of cell events
        """
        self.position_x = position[0]  # type: float
        self.position_y = position[1]  # type: float
        self.position_z = position[2]  # type: float
        self.position_delta_x = 0  # type: float
        self.position_delta_y = 0  # type: float
        self.radius = radius  # type: float
        self.max_radius = 25  # type: float
        self.target_radius = 25  # type: float
        self.dividable = True  # type: bool
        self.growth_rate = .01  # type: float
        self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        if support_specializations is None:
            self.support_specializations = set()  # type: set
        else:
            self.support_specializations = support_specializations  # type: set

        # This is a set of the functions which are passively run on this cell during the
        # Epithelium.update functions.  They are added by furrow events.
        if cell_events is None:
            self.cell_events = set([])  # type: set
        else:
            self.cell_events = cell_events  # type: set

    def divide(self):
        """
        Divides this cell into a new cell with half of this cell's radius.
        Then divides this parent cell's radius in half.
        :return:
        """
        # Choose some radian for direction of placement of new cell
        rand_rad = random.uniform(0, 6.283)
        # Find position for new cell on original cell's circle
        delta_x = self.radius/2 * cos(rand_rad)
        delta_y = self.radius/2 * sin(rand_rad)
        rand_pos = (self.position_x + delta_x, self.position_y + delta_y, 0)
        child_cell = Cell(position=rand_pos, radius=self.radius / 2.0, cell_events=set(self.cell_events))
        child_cell.growth_rate = self.growth_rate
        child_cell.max_radius = self.max_radius
        # Divide the original cell size in half
        self.radius /= 2
        # Move the parent cell to complete the division
        self.position_x -= delta_x
        self.position_y -= delta_y
        return child_cell

    def grow(self, growth_amount=None):
        """
        Increases the cell's radius by growth_amount or its internal growth_rate when no input is provided
        :param growth_amount: The amount to grow the radius
        :return:
        """
        self.radius += growth_amount if growth_amount else self.growth_rate

    def shrink(self, growth_amount=None):
        """
        Decreases the cell's radius by growth_amount or its internal growth_rate when no input is provided
        :param growth_amount: The amount to shrink the radius
        :return:
        """
        self.radius -= growth_amount if growth_amount else self.growth_rate

    def dispatch_updates(self):
        """
        Calls all functions in the cell_updaters function list.
        :return:
        """
        for updater in self.cell_events:
            updater(self)

    def distance_to_other(self, neighbor):
        """
        Calculates the distance between this cell and another cell
        :param neighbor: The distance to this cell will be found.
        :return: the distance between this cell and the passed neighbor cell.
        """
        (x1, y1, z1) = (self.position_x, self.position_y, self.position_z)
        (x2, y2, z2) = (neighbor.position_x, neighbor.position_y, neighbor.position_z)
        return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

    def touches(self, neighbor) -> bool:
        """
        Returns true if the passed cell is colliding with this one
        :param neighbor: Cell to check for collision
        :return: True if the cells collide. False otherwise.
        """
        if self.distance_to_other(neighbor) <= self.radius + neighbor.radius:
            return True
        return False
