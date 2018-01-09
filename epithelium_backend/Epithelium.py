

import random

from epithelium_backend import Cell
from epithelium_backend import SpringSimulator


class Epithelium(object):
    """A collection of cells that will form an eye"""

    def __init__(self, cell_quantity,
                 cell_radius_divergence: float = .5,
                 cell_avg_radius: float = 4) -> None:
        """
        Initializes the epithelium
        :param cell_quantity: number of cells to be in the sheet
        :param cell_radius_divergence: divergence of cell radii, a multiplier of cell_avg_radius
        :param cell_avg_radius: average cell radius
        """
        self.cells = []
        self.cell_quantity = cell_quantity
        self.cell_radius_divergence = cell_radius_divergence
        self.cell_avg_radius = cell_avg_radius

        self.create_cell_sheet()

    def divide_cell(self, cell_from_list) -> None:
        """
        divides the given cell and adds it to the list
        :param cell_from_list: a cell selected from self.cells
        """
        new_cell = cell_from_list.divide()
        if new_cell is not None:
            self.cells.append(new_cell)

    def create_cell_sheet(self) -> None:
        """
        creates the sheet of cells, populating self.cells, and then decompacts them
        """
        while self.cell_quantity > len(self.cells):

            # Use the divergence to determine the new cells' radii. Note that the cell_radius_divergence should be
            # less than cell_avg_radius
            rand_radius = self.cell_avg_radius * random.uniform(self.cell_avg_radius - self.cell_radius_divergence,
                                                                self.cell_avg_radius + self.cell_radius_divergence)
            random_pos = (random.random() * 10, random.random() * 10, 0)
            self.cells.append(Cell.Cell(position=random_pos, radius=rand_radius))

        # Decompact 1000 times with kind of arbitrary parameters
        SpringSimulator.decompact(self.cells, iterations=1000, spring_constant=1, escape=1.05, dt=0.1)
