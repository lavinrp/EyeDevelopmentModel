

from epithelium_backend import Cell
from epithelium_backend import CellType


class Epithelium(object):
    """A collection of cells that will form an eye"""

    def __init__(self, cell_quantity):
        """
        Initializes the epithelium
        :param cell_quantity: number of cells to be in the sheet
        """
        self.cells = []
        self.cell_events = []
        self.cell_quantity = cell_quantity

        self.create_cell_sheet()

    def create_cell_sheet(self):
        """
        creates the sheet of cells, populating self.cell
        """
        self.cells.append(Cell)

        # should be made parallel
        while len(self.cells) < self.cell_quantity:
            self.cells[0].divide()
