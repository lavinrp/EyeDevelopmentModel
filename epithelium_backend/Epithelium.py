

import random

from epithelium_backend import Cell
from epithelium_backend import SpringSimulator


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

    def add_cell(self, cell_from_list):
        """
        adds a cell to the list
        """
        new_cell = cell_from_list.divide()
        if new_cell is not None:
            self.cells.append(new_cell)

    def create_cell_sheet(self):
        """
        creates the sheet of cells, populating self.cell
        """
        print('We have added the first cell:')

        while self.cell_quantity > len(self.cells):

            self.cells.append(Cell.Cell(position=(random.random(), random.random(), 0), radius=random.uniform(.06, .1), cell_types=[]))

        # Plot the cells as they were spawned
        SpringSimulator.plot(self.cells, 'before.png')

        # Decompact with kind of arbitrary parameters
        for i in range(0, 5):
            SpringSimulator.decompact(testEpithelium.cells, iterations=300, spring_constant=1, escape=1.05, dt=0.1)
            SpringSimulator.plot(self.cells, 'before.png')

        print('We have done the mapping')

        print(len(self.cells))


if __name__ == '__main__':
    testEpithelium = Epithelium(300)

    testEpithelium.create_cell_sheet()



