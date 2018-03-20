from epithelium_backend import Cell
from epithelium_backend import Epithelium


class PassiveGrowth(object):
    """
    A default cell event.
    Functor which will passively grow a given cell.
    """

    def __init__(self, epithelium: Epithelium):
        self.epithelium = epithelium

    def __call__(self, cell: Cell):
        """
        If this cell's radius is at least the maximum radius for a cell, then calls spawn_new_cell. Otherwise, it will
        grow by the cell's growth rate.
        :return:
        """
        # Check if cell is large enough to divide
        if cell.radius < cell.max_radius:
            # If not large enough, grow the cell a little bit for next time
            cell.grow_cell(cell.growth_rate)
        else:
            # If the cell is large enough and allowed to be divided, then we will divide the cell
            self.epithelium.divide_cell(cell)
