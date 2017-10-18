from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.SupportCellType import SupportCellType
import random as random


class Cell(object):
    """A single cell"""
    def __init__(self, position=(0.5, 0.5, 0.0), radius=10.0, cell_types=[]):
        """
        Initializes this instance of the Cell class
        :param: The cartesian coordinates of the cell (x,y,z)
        :param: The radius of the cell
        :param: The cells photoreceptor specialization
        :param: Set of the cells non-photoreceptor specializations
        """
        self.position = position  # type: tuple
        self.radius = radius  # type: float
        # self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        # self.support_specializations = support_specializations  # type: set

    def divide(self):
        (x,y, z) = self.position
        random_position=(x+(0.5-random.random())/5,
                         y+(0.5-random.random())/5,
                         0)
        radius = (0.2 + random.random()/4)/2
        child_cell = Cell(position=random_position, radius=radius)
        return child_cell
