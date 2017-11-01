from epithelium_backend import Cell
from epithelium_backend import SpringDemo
from epithelium_backend import CellCollisionHandler
from epithelium_backend import R8Selector
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
        start = time.time()
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
        print((avg_area, approx_grid_size))
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
        SpringDemo.plot(self.cells, 'im/before0.png',grid=6)
        decompact_start = time.time()
        for i in range(0,5):
            print(i)
            for j in range(0,19):
                self.cell_collision_handler.decompact()
            # SpringDemo.plot(self.cells, 'im/before'+(str(i+1))+'.png',grid=7)

        end = time.time()
        # SpringDemo.plot(self.cells, 'im/before0.png',grid=7)
        print('total time = ' + str(end-start))
        print('decompaction time = ' + str(end-decompact_start))

    def R8Demo(self):
        selector = R8Selector.R8Selector(6*0.2)
        # i = 0
        # j = 0
        for cell in self.cell_collision_handler.posterior_to_anterior():
            # if i % (len(self.cells)/10) == 0:
            #     SpringDemo.plot(self.cells, 'im/r8'+str(j)+'.png', grid=7)
            #     j+=1
            # i +=1
            selector(self, cell)
        # SpringDemo.plot(self.cells, 'im/r8'+str(j)+'.png', grid=7)
        # print(i)

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
        # ns = [len(v) for k,v in ig.nodes.items()]
        # ns.sort()
        # print('avg = ' + (str(sum(ns)/len(ns))))
        # print('max = ' + (str(max(ns))))
        # print('min = ' + (str(min(ns))))
        # print('mode = ' + (str(ns[int(len(ns)/2)])))


# if __name__ == '__main__':
#     testEpithelium = Epithelium(20)
#     testEpithelium.create_cell_sheet()

#     # Decompact 250 times with kind of arbitrary parameters
#     SpringSimulator.decompact(testEpithelium.cells, iterations=250, spring_constant=8, escape=1.05)
#     # Plot the cells after being decompacted
#     SpringSimulator.plot(testEpithelium.cells, 'after.png')
