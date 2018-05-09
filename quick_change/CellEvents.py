from epithelium_backend import Cell
from epithelium_backend import Epithelium

import random


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


class TryCellDeath(object):
    """
    Functor which has a percent chance to kill a given cell
    """

    def __init__(self, epithelium: Epithelium, death_chance: float=0.1):
        """

        :param epithelium: the epithelium that this event will operate on
        :param death_chance: the chance of this functor killing a cell (1 is 100%, 0.5 is 50%, etc)
        """
        self.epithelium = epithelium
        if death_chance < 0 or death_chance > 1:
            raise ValueError('TryCellDeath.death_chance must be a float within the range [0, 1]')

        self.death_chance = death_chance

    def __call__(self, cell: Cell) -> None:
        """
        Attempt to kill the passed cell
        :param cell: The cell to attempt to kill
        """

        if random.random() <= self.death_chance:
            self.epithelium.delete_cell(cell)
