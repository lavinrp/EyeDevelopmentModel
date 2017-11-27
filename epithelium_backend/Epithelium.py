from epithelium_backend import Cell
from epithelium_backend import CellCollisionHandler
from math import sqrt
from random import random
import time as time

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
        self.cell_collision_handler = None
        self.create_cell_sheet()

    def add_cell(self, cell_from_list):
        """
        adds a cell to the list
        """
        if len(self.cells) < self.cell_quantity:
            new_cell = cell_from_list.divide()
            self.cells.append(new_cell)
            return new_cell

    def create_cell_sheet(self):
        """
        creates the sheet of cells, populating self.cell
        """
        # The approach: randomly place self.cell_quantity cells on a grid,
        # then decompact them with the collision handler until they're
        # just slightly overlapping.

        # If we know the average radius of each cell, we know the average
        # area, and therefore the approximate grid size.
        avg_radius = 0.2
        avg_area = avg_radius * avg_radius * 3.14
        # Because we allow some cell overlap, and we want the cells to start
        # in a more compact state and decompact them, we multiply by .87
        approx_grid_size = 0.87 * sqrt(avg_area*self.cell_quantity)
        for i in range(0,self.cell_quantity):
            # if approx_grid_size is 5, that means cells will be x values
            # between -2.5 and 2.5, and y values between -2.5 and 2.5,
            # and be uniformly distributed.
            x = (0.5 - random()) * approx_grid_size
            y = (0.5 - random()) * approx_grid_size
            # radius between 0.195 - 0.205
            radius = 0.2 + ((0.5 - random()) * 0.1)
            self.cells.append(Cell.Cell((x,y,0), radius))
        self.cell_collision_handler = CellCollisionHandler.CellCollisionHandler(self.cells)
        for i in range(0,5):
            for j in range(0,9):
                self.cell_collision_handler.decompact()


    def stats(self):
        """
        Print stats on the collision handler. Just for testing.
        """
        ig = self.cell_collision_handler
        grids = ig.grids
        non_empty = list(filter(lambda x : len(x)>0, grids))
        print('avg = ' + str(sum(map(len, non_empty))/len(non_empty)))
        print('filled ratio = ' + str(len(non_empty)/len(grids)))
        print('max = ' + str(max(map(len, non_empty))))
