from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.PigmentType import PigmentType


class Cell(object):
    """A single cell"""
    def __init__(self,
                 position=(0, 0, 0),
                 radius=1,
                 photoreceptor_type=PhotoreceptorType.NOT_RECEPTOR,
                 pigment_type=PigmentType.NO_PIGMENT):
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: The radius of the cell
        :param photoreceptor_type: The cells photoreceptor specialization
        :param pigment_type: The cells pigmentation specialization
        """
        self.position = position
        self.radius = radius
        self.photoreceptor_type = photoreceptor_type
        self.pigment_type = pigment_type

    def divide(self):
        pass
