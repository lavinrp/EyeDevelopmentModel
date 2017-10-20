

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
        first_cell = Cell.Cell(position=(0.2, 0.2, 0), radius=.2, cell_types=[])
        self.cells.append(first_cell)
        print('We have added the first cell:')

        while self.cell_quantity > len(self.cells):
            # Plot the cells as they were spawned
            SpringSimulator.plot(self.cells, 'before.png')
            for cell in self.cells:
                # Decompact with kind of arbitrary parameters
                SpringSimulator.decompact(testEpithelium.cells, iterations=20, spring_constant=1, escape=1.05, dt=0.1)

                if self.cell_quantity > len(self.cells):
                    self.add_cell(cell)

        print('We have done the mapping')

        print(len(self.cells))


if __name__ == '__main__':
    testEpithelium = Epithelium(50)

    testEpithelium.create_cell_sheet()



