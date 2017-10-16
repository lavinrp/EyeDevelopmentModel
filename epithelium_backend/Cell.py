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
        :param: The cartesian coordinates of the cell (x,y,z)
        :param: The radius of the cell
        :param: The cells photoreceptor specialization
        :param: Set of the cells non-photoreceptor specializations
        """
        self.position = position  # type: tuple
        self.radius = radius  # type: float
        self.photoreceptor_type = photoreceptor_type  # type: photoreceptor_type
        self.support_specializations = support_specializations  # type: set

    def divide(self):
        pass
