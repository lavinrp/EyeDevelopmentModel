import random
from math import sqrt

from epithelium_backend import Cell
from epithelium_backend import CellCollisionHandler
from epithelium_backend.CellFactory import CellFactory
from epithelium_backend import Furrow
from quick_change.FurrowEventList import furrow_event_list
from quick_change import CellEvents


class Epithelium(object):
    """A collection of cells that will form an eye"""

    def __init__(self, cell_quantity: int,
                 cell_avg_radius: float = 10,
                 cell_factory: CellFactory = None) -> None:
        """
        Initializes the epithelium
        :param cell_quantity: number of cells to be in the sheet
        :param cell_avg_radius: average cell radius
        :param cell_factory: A factory responsible for producing the initial cells in the epithelium.
        """
        self.cells = []
        self.cell_quantity = cell_quantity
        self.cell_avg_radius = cell_avg_radius
        self.cell_collision_handler = None

        self.create_cell_sheet(cell_factory)

        # create furrow
        if len(self.cells):
            furrow_initial_position = max(map(lambda c: c.position_x, self.cells))
        else:
            furrow_initial_position = 0

        self.furrow = Furrow.Furrow(position=furrow_initial_position,
                                    velocity=1,
                                    events=furrow_event_list)

    def divide_cell(self, cell_from_list) -> Cell:
        """
        divides the given cell and adds the newly created cell to the list
        :param cell_from_list: a cell selected from self.cells
        :return: The newly created cell or None if the cell could not be divided.
        """

        if cell_from_list.dividable:
            new_cell = cell_from_list.divide()
            if new_cell is not None:
                self.cells.append(new_cell)
                self.cell_collision_handler.register(new_cell)
            return new_cell
        return None

    def delete_cell(self, cell: Cell):
        """
        Removes a cell from the epithelium, and then deregisters it from the CellCollisionHandler
        :param cell: cell to delete from the epithelium
        :return:
        """
        self.cells.remove(cell)
        self.cell_collision_handler.deregister(cell)

    def create_cell_sheet(self, cell_factory: CellFactory = None) -> None:
        """
        creates the sheet of cells, populating self.cells, and then decompacts them
        :param cell_factory: A factory responsible for producing the initial cells in the new cell sheet.
        """

        # ensure presence of valid factory
        if cell_factory is None:
            cell_factory = CellFactory()

        # This is the list of functions which are each cell should start out with.
        # They are run once per tick of the simulation.
        default_cell_events = {CellEvents.PassiveGrowth(self)}

        # create cells for sheet
        cell_factory.cell_events = default_cell_events
        self.cells = cell_factory.create_cells(self.cell_quantity)

        # run initial decompaction of cells cells
        if self.cell_quantity > 0:
            self.cell_collision_handler = CellCollisionHandler.CellCollisionHandler(self.cells)
            for i in range(0, 50):
                self.cell_collision_handler.decompact()

    def neighboring_cells(self, cell: Cell, number_cells: int):
        """
        Return every cell within a given number of cells.
        :param cell: The target cell. This cells neighbors will be returned.
        :param number_cells: an integer, the number of average cell radii.
        """
        # Multiply by average diameter to convert cell count into distance.
        # Distance is edge to edge, rather than center to center, hence
        # the number_cells+1.
        dist = (number_cells+1)*2*self.cell_avg_radius
        return self.cell_collision_handler.cells_within_distance(cell, dist)

    def update(self):
        """Simulates the epithelium for one tick"""
        self.furrow.update(self)
        self.run_cell_updates()
        self.cell_collision_handler.decompact()

    def run_cell_updates(self):
        """
        Has each cell run all of their respective updating functions.
        :return:
        """
        for cell in self.cells:
            cell.dispatch_updates()
