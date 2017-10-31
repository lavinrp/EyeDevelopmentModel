

import random

from epithelium_backend import Cell
from epithelium_backend import SpringSimulator


class Epithelium(object):
    """A collection of cells that will form an eye"""

    def __init__(self, cell_quantity) -> None:
        """
        Initializes the epithelium
        :param cell_quantity: number of cells to be in the sheet
        """
        self.cells = []
        self.cell_events = []
        self.cell_quantity = cell_quantity

        self.create_cell_sheet()

    def add_cell(self, cell_from_list) -> None:
        """
        adds a cell to the list
        :param cell_from_list: a cell selected from self.cells
        """
        new_cell = cell_from_list.divide()
        if new_cell is not None:
            self.cells.append(new_cell)

    def create_cell_sheet(self) -> None:
        """
        creates the sheet of cells, populating self.cell, and then decompacts them
        """

        while self.cell_quantity > len(self.cells):
            random_radius = 10 + random.random() * 4
            random_pos = (249 + random.random() * 5, 249 + random.random() * 5, 0)
            self.cells.append(Cell.Cell(position=random_pos, radius=random_radius))

        # Decompact 1000 times with kind of arbitrary parameters
        SpringSimulator.decompact(self.cells, iterations=1000, spring_constant=1, escape=1.05, dt=0.1)
