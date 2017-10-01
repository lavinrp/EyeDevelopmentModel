from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.SupportCellType import SupportCellType


class Cell(object):
    """A single cell"""
    def __init__(self,
                 position=(0, 0, 0),
                 radius=1,
                 photoreceptor_type=PhotoreceptorType.NOT_RECEPTOR,
                 support_specializations=set()):
        """
        Initializes this instance of the Cell class
        :param tuple position: The cartesian coordinates of the cell (x,y,z)
        :param float radius: The radius of the cell
        :param PhotoreceptorType photoreceptor_type: The cells photoreceptor specialization
        :param set[SupportCellType] support_specializations: Set of the cells
         non-photoreceptor specializations
        """
        self.position = position  # type: tuple
        self.radius = radius  # type: float
        self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        self.support_specializations = support_specializations  # type: set[SupportCellType]

    def divide(self):
        pass
