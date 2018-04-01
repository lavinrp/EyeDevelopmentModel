import unittest

from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.Cell import Cell
from epithelium_backend.CellCollisionHandler import distance
from epithelium_backend.CellCollisionHandler import CellCollisionHandler
from epithelium_backend.CellFactory import CellFactory


class EpitheliumTester(unittest.TestCase):

    def test_init(self):
        """Ensures that Epithelium instances are initialized correctly."""
        # check epithelium values
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)
        self.assertEqual(epithelium.cell_quantity, cell_quantity,
                         "Epithelium.cell_quantity incorrectly set in Epithelium.__init__")
        self.assertEqual(epithelium.cell_avg_radius, cell_avg_radius,
                         "epithelium.cell_avg_radius incorrectly set in Epithelium.__init__")
        self.assertEqual(len(epithelium.cells), cell_quantity,
                         "Incorrect number of cells generated in Epithelium.__init__")

        # check furrow values
        furrow_initial_position = max(map(lambda c: c.position_x, epithelium.cells))
        self.assertEqual(epithelium.furrow.position, furrow_initial_position,
                         "Furrow incorrectly placed in Epithelium.__init__")

    def test_divide_cell(self):
        """Ensures that Epithelium instances can correctly divide their cells."""
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)
        original_size = epithelium.cells[0].radius
        epithelium.divide_cell(epithelium.cells[0])
        self.assertEqual(len(epithelium.cells), cell_quantity + 1, "Incorrect cell count after Epithelium.divide_cell.")
        self.assertAlmostEqual(original_size/2,
                               epithelium.cells[0].radius,
                               3,
                               "Incorrect cell size after Epithelium.divide_cell.")

    def test_divide_cell_not_dividable(self):

        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)
        epithelium.cells[0].dividable = False  # ensure that the cell cannot divide.
        original_size = epithelium.cells[0].radius
        epithelium.divide_cell(epithelium.cells[0])
        self.assertEqual(len(epithelium.cells), cell_quantity,
                         "Epithelium.divide_cell divided a cell that was not dividable")
        self.assertAlmostEqual(original_size,
                               epithelium.cells[0].radius,
                               3,
                               "Epithelium.divide_cell incorrectly changed cell size after failed divide.")

    def test_delete_cell(self):
        cell_quantity = 10
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)

        # delete the cell
        cell_to_delete = epithelium.cells[1]
        epithelium.delete_cell(cell_to_delete)

        self.assertNotIn(cell_to_delete, epithelium.cells,
                         "Epithelium.delete_cell does not remove cell from epithelium")
        self.assertNotIn(cell_to_delete, epithelium.cell_collision_handler.cells,
                         "Epithelium.delete_cell does not deregester cell from collision handler.")

    def test_create_cell_sheet(self):
        """Ensures that instances of Epithelium can correctly populate their cell lists on init."""
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)

        # ensure that the created cells match the input parameters
        for cell in epithelium.cells:
            self.assertAlmostEqual(cell.radius, cell_avg_radius, delta=cell_radius_divergence * cell_avg_radius,
                                   msg="Incorrect cell radii produced by Epithelium.create_cell_sheet.")

    def test_create_cell_sheet_rerun(self):
        """Ensures that an Epithelium can correctly populate its cell with additional cells after init."""
        cell_quantity = 1
        cell_radius_divergence = .1
        cell_avg_radius = 1
        cell_factory = CellFactory()
        cell_factory.radius_divergence = cell_radius_divergence
        cell_factory.average_radius = cell_avg_radius
        epithelium = Epithelium(cell_quantity, cell_avg_radius, cell_factory)

        # set the new number of cells
        new_cell_quantity = 19
        epithelium.cell_quantity = new_cell_quantity
        epithelium.create_cell_sheet(cell_factory)

        # ensure that there are the correct number of cells
        self.assertEqual(len(epithelium.cells), new_cell_quantity,
                         "Incorrect cell count after Epithelium.create_cell_sheet")

        # ensure that the created cells match the input parameters
        for cell in epithelium.cells:
            self.assertAlmostEqual(cell.radius, cell_avg_radius, delta=cell_radius_divergence * cell_avg_radius,
                                   msg="Incorrect cell radii produced by Epithelium.create_cell_sheet")

    def test_neighboring_cells(self):
        """Ensures that Epithelium.neighboring_cells returns the correct neighbors."""
        cell_quantity = 5
        cell_radius = 5
        epithelium = Epithelium(cell_quantity=0, cell_avg_radius=cell_radius)
        cell_dist = 10

        # create cells for epithelium
        cells = []
        for i in range(cell_quantity):
            cell = Cell(position=(i * cell_dist, 0, 0), radius=cell_radius)
            cells.append(cell)
        epithelium.cells = cells
        epithelium.cell_collision_handler = CellCollisionHandler(epithelium.cells)

        radii_between_neighbors = 8
        neighbors_of_first_cell = []
        cell = cells[0]
        for other in cells:
            if cell is not other:
                if distance((cell.position_x,
                             cell.position_y,
                             cell.position_z),
                            (other.position_x,
                             other.position_y,
                             other.position_z)) <= (radii_between_neighbors * cell_radius):
                    neighbors_of_first_cell.append(other)

        returned_neighbors = list(epithelium.neighboring_cells(cell, radii_between_neighbors))

        self.assertListEqual(neighbors_of_first_cell, returned_neighbors,
                             "Incorrect neighbors returned by Epithelium.neighboring_cells")

    def test_update(self):
        """ Ensures that updating the epithelium updates the cells and the furrow.
        :return:
        """

        cell_quantity = 2
        cell_radius = 5
        epithelium = Epithelium(cell_quantity=0, cell_avg_radius=cell_radius)
        cell_dist = 1

        # create cells for epithelium
        cells = []
        for i in range(cell_quantity):
            cell = Cell(position=(i * cell_dist, 0, 0), radius=cell_radius)
            cells.append(cell)
        epithelium.cells = cells
        epithelium.cell_collision_handler = CellCollisionHandler(epithelium.cells)

        # initial states
        initial_furrow_pos = epithelium.furrow.position
        cell_0_position = (cells[0].position_x, cells[0].position_y)
        cell_1_position = (cells[1].position_x, cells[1].position_y)

        # update epithelium
        epithelium.update()

        # check that cells have moved
        self.assertNotEqual((cells[0].position_x, cells[0].position_y), cell_0_position,
                            "Cell 0 position not changed when updating epithelium in Epithelium.update")
        self.assertNotEqual((cells[1].position_x, cells[1].position_y), cell_1_position,
                            "Cell 1 position not changed when updating epithelium in Epithelium.update")

        # check furrow
        self.assertEqual(epithelium.furrow.position, initial_furrow_pos - epithelium.furrow.velocity,
                         "Furrow position not correctly changed when updating epithelium in Epithelium.update")
