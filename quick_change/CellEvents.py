from epithelium_backend import Cell
from epithelium_backend import Epithelium


class PassiveGrowth(object):
    """
    A default cell event.
    Functor which will passively grow a given cell.
    """

    def __init__(self, epithelium: Epithelium):
        self.epithelium = epithelium

    def __call__(self, cell: Cell) -> None:
        """
        If passed cell's radius is less than its max_radius, it will grow by the cell's growth rate.  Otherwise, it
        will check if the cell is allowed to be divided and then divide it.
        :param cell: The cell to grow.
        """
        # Check if cell is small enough to grow
        if cell.radius < cell.max_radius:
            # If not large enough, grow the cell a little bit for next time
            cell.grow_cell(cell.growth_rate)
        else:
            # If the cell is large enough and allowed to be divided, then we will divide the cell
            self.epithelium.divide_cell(cell)
