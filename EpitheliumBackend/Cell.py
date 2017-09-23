

class Cell(object):
    """A single cell"""
    def __init__(self, position=(0, 0, 0), radius=10, cell_types=[]):
        """
        Initializes this instance of the Cell class
        :param position: The cartesian coordinates of the cell (x,y,z)
        :param radius: The radius of the cell
        :param cell_types: The cells specializations
        """
        self.position = position
        self.radius = radius
        self.cell_types = cell_types

    def divide(self):
        pass
