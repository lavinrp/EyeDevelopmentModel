from epithelium_backend.Cell import Cell

import random
from math import sqrt
import math
import copy


class CellFactory(object):
    """Factory pattern for neatly generating multiple similar cells"""

    def __init__(self):
        """Initializes the CellFactory"""
        self.max_radius = 25
        self.growth_rate = 0.01
        self.cell_events = set()
        self.radius_divergence = 0.5
        self.average_radius = 10

    def create_cells(self, quantity: int) -> list:
        """
        Creates a list of cells with the factories parameters.
        :param quantity: The number of cells to create.
        :return: A list of newly generated cells.
        """
        # The approach: randomly place self.cell_quantity cells on a grid,
        # then decompact them with the collision handler until they're
        # just slightly overlapping.

        # If we know the average radius of each cell, we know the average
        # area, and therefore the approximate grid size.
        avg_area = self.average_radius ** 2 * math.pi
        # Because we allow some cell overlap, and we want the cells to start
        # in a more compact state and decompact them, we multiply by .87
        approx_grid_size = 0.87 * sqrt(avg_area * quantity)

        # build cell list
        cells = []
        for i in range(quantity):
            # cell_radius_divergence is a percentage, like 0.05 (5%). So you want to
            # uniformly grab radii within +/- cell_radius_divergence percent of cell_avg_radius
            rand_radius = random.uniform(self.average_radius * (1 - self.radius_divergence),
                                         self.average_radius * (1 + self.radius_divergence))
            random_pos = (random.random() * approx_grid_size,
                          random.random() * approx_grid_size,
                          0)

            # create the cell
            cell_events = copy.deepcopy(self.cell_events)
            cell = Cell(position=random_pos,
                        radius=rand_radius,
                        cell_events=cell_events)
            cell.max_radius = self.max_radius
            cell.growth_rate = self.growth_rate
            cells.append(cell)

        return cells
