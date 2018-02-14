import random
from math import sqrt

from epithelium_backend import Cell
from epithelium_backend import CellCollisionHandler
from epithelium_backend import Furrow
from epithelium_backend.FurrowEventList import furrow_event_list


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
        self.cell_collision_handler = None

        self.create_cell_sheet()

        # create furrow
        if len(self.cells):
            furrow_initial_position = max(map(lambda c: c.position_x, self.cells))
        else:
            furrow_initial_position = 0

        self.furrow = Furrow.Furrow(position=furrow_initial_position,
                                    velocity=self.cell_avg_radius * 6,
                                    events=furrow_event_list)

    def divide_cell(self, cell_from_list) -> None:
        """
        divides the given cell and adds it to the list
        :param cell_from_list: a cell selected from self.cells
        """
        new_cell = cell_from_list.divide()
        if new_cell is not None:
            self.cells.append(new_cell)
            self.cell_collision_handler.register(new_cell)

    def create_cell_sheet(self) -> None:
        """
        creates the sheet of cells, populating self.cells, and then decompacts them
        """
        # The approach: randomly place self.cell_quantity cells on a grid,
        # then decompact them with the collision handler until they're
        # just slightly overlapping.

        # If we know the average radius of each cell, we know the average
        # area, and therefore the approximate grid size.
        avg_area = self.cell_avg_radius**2 * 3.14
        # Because we allow some cell overlap, and we want the cells to start
        # in a more compact state and decompact them, we multiply by .87
        approx_grid_size = 0.87 * sqrt(avg_area*self.cell_quantity)
        while self.cell_quantity > len(self.cells):

            # cell_radius_divergence is a percentage, like 0.05 (5%). So you want to
            # uniformly grab radii within +/- cell_radius_divergence percent of cell_avg_radius
            rand_radius = random.uniform(self.cell_avg_radius*(1-self.cell_radius_divergence),
                                         self.cell_avg_radius*(1+self.cell_radius_divergence))
            random_pos = (random.random() * approx_grid_size,
                          random.random() * approx_grid_size,
                          0)
            self.cells.append(Cell.Cell(position=random_pos, radius=rand_radius))

        if self.cell_quantity > 0:
            self.cell_collision_handler = CellCollisionHandler.CellCollisionHandler(self.cells)
            for i in range(0,50):
                self.cell_collision_handler.decompact()

    def neighboring_cells(self, cell: Cell, number_cells: int):
        """
        Return every cell within a given number of cells.
        :param cell: The target cell. This cells neighbors will be returned.
        :param number_cells: an integer, the number of average cell radii.
        """
        return self.cell_collision_handler.cells_within_distance(cell, number_cells*self.cell_avg_radius)

    def go(self):
        """
        Start the simulation, run the furrow for 10 steps. (Just for demo).
        """

        for i in range(0, 10):
            self.furrow.update(self)

    def update(self):
        """Simulates the epithelium for one tick"""
        self.furrow.update(self)
        self.cell_collision_handler.decompact()
