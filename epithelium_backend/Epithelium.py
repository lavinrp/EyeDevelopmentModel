

import random

from epithelium_backend import Cell
from epithelium_backend import SpringSimulator
from display_2d.SnapshotDisplay import SnapshotDisplay


class Epithelium(object):
    """A collection of cells that will form an eye"""

    def __init__(self, cell_quantity, cell_radius_divergence) -> None:
        """
        Initializes the epithelium
        :param cell_quantity: number of cells to be in the sheet
        :param cell_radius_divergence: divergence of cell radii, a multiplier of cell_magic_radius
        """
        self.cells = []
        self.cell_events = []
        self.cell_quantity = cell_quantity
        self.cell_radius_divergence = cell_radius_divergence
        self.cell_avg_radius = 4

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
            # random_radius = 10 + (random.random() * 100)/2
            rand_radius = self.cell_avg_radius * random.uniform(self.cell_avg_radius - self.cell_radius_divergence,
                                                                self.cell_avg_radius + self.cell_radius_divergence)
            random_pos = (245 + random.random() * 10, 240 + random.random() * 10, 0)
            self.cells.append(Cell.Cell(position=random_pos, radius=rand_radius))

        # Plot the cells as they were spawned
        SnapshotDisplay("epithelium demo before ", (500, 500), self.cells)
        # Decompact 250 times with kind of arbitrary parameters
        SpringSimulator.decompact(self.cells, iterations=1000, spring_constant=1, escape=1.05, dt=0.1)
        # Plot the cells after being decompacted
        SnapshotDisplay("epithelium demo after", (500, 500), self.cells)
