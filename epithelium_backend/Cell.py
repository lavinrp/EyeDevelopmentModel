
import random
from math import sin, cos

from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.SupportCellType import SupportCellType


class Cell(object):
    """A single cell"""
    def __init__(self,
                 position: tuple = (0, 0, 0),
                 radius: float = 1,
                 photoreceptor_type: PhotoreceptorType = PhotoreceptorType.NOT_RECEPTOR,
                 support_specializations: set = set()) -> None:
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: A multiplier of the average cell radius
        :param photoreceptor_type: The cells photoreceptor specialization
        :param support_specializations: Set of the cells non-photoreceptor specializations
        """
        self.position = position  # type: tuple
        self.radius = radius  # type: float
        self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        self.support_specializations = support_specializations  # type: set

    def divide(self):
        """
        If this cell's radius is large enough, divides this cell into a new cell with
        half of this cell's radius. Then divides this parent cell's radius in half.
        :return:
        """
        # Choose some radian for direction of position of new cell
        rand_rad = random.uniform(0, 6.283)
        # Check if cell is large enough to divide
        if self.radius >= 25:
            # Find position for new cell on original cell's circle
            rand_pos = (self.position[0] + self.radius*cos(rand_rad), self.position[0] + self.radius*sin(rand_rad), 0)
            child_cell = Cell(position=rand_pos, radius=self.radius/2.0)
            new_pos = (self.position[0] - self.radius*cos(rand_rad), self.position[0] - self.radius*sin(rand_rad), 0)
            self.position = new_pos
            self.radius /= 2
            return child_cell
        else:
            # If not large enough, grow the cell a little bit for next time
            self.radius += rand_rad/100
            return None
