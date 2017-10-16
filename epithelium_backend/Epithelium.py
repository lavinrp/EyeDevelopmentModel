
# from multiprocessing import Pool, Lock

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

        self.create_cell_sheet()

    def add_cell(self, cell_from_list):
        """
        adds a cell to the list
        """
        if len(self.cells) < self.cell_quantity:
            new_cell = cell_from_list.divide()
            self.cells.append(new_cell)

    def create_cell_sheet(self):
        """
        creates the sheet of cells, populating self.cell
        """
        first_cell = Cell.Cell(position=(0.2, 0.2, 0.2), radius=.2, cell_types=[])
        second_cell = Cell.Cell(position=(0.3, 0.3, 0.3), radius=.2, cell_types=[])
        self.cells.append(first_cell)
        self.cells.append(second_cell)
        print('We have added the first cell:')

        while self.cell_quantity > len(self.cells):
            for cell in self.cells:
                self.add_cell(cell)

        print('We have done the mapping')

        print(len(self.cells))


if __name__ == '__main__':
    testEpithelium = Epithelium(20)
    testEpithelium.create_cell_sheet()

    # Plot the cells as they were spawned
    SpringSimulator.plot(testEpithelium.cells, 'before.png')
    # Decompact 250 times with kind of arbitrary parameters
    SpringSimulator.decompact(testEpithelium.cells, iterations=500000, spring_constant=8, escape=1, dt=1)
    # Plot the cells after being decompacted
    SpringSimulator.plot(testEpithelium.cells, 'after.png')


