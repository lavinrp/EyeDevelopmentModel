import unittest

from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.CellCollisionHandler import distance


class EpitheliumTester(unittest.TestCase):

    def test_init(self):
        """Ensures that Epithelium instances are initialized correctly."""
        # check epithelium values
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        epithelium = Epithelium(cell_quantity, cell_radius_divergence, cell_avg_radius)
        self.assertEqual(epithelium.cell_quantity, cell_quantity, "Epithelium.cell_quantity incorrectly set.")
        self.assertEqual(epithelium.cell_radius_divergence, cell_radius_divergence,
                         "epithelium.cell_radius_divergence incorrectly set.")
        self.assertEqual(epithelium.cell_avg_radius, cell_avg_radius, "epithelium.cell_avg_radius incorrectly set.")
        self.assertEqual(len(epithelium.cells), cell_quantity, "Incorrect number of cells generated.")

        # check furrow values
        furrow_initial_position = max(map(lambda c: c.position_x, epithelium.cells))
        self.assertEqual(epithelium.furrow.position, furrow_initial_position, "Furrow incorrectly placed on init.")

    def test_divide_cell(self):
        """Ensures that Epithelium instances can correctly divide their cells."""
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        epithelium = Epithelium(cell_quantity, cell_radius_divergence, cell_avg_radius)
        original_size = epithelium.cells[0].radius
        epithelium.divide_cell(epithelium.cells[0])
        self.assertEqual(len(epithelium.cells), cell_quantity + 1, "Incorrect cell count after Epithelium.divide_cell.")
        self.assertAlmostEqual(original_size/2,
                               epithelium.cells[0].radius,
                               3,
                               "Incorrect cell size after Epithelium.divide_cell.")

    def test_create_cell_sheet(self):
        """Ensures that instances of Epithelium can correctly populate their cell lists on init."""
        cell_quantity = 19
        cell_radius_divergence = .1
        cell_avg_radius = 1
        epithelium = Epithelium(cell_quantity, cell_radius_divergence, cell_avg_radius)

        # ensure that the created cells match the input parameters
        for cell in epithelium.cells:
            self.assertAlmostEqual(cell.radius, cell_avg_radius, delta=cell_radius_divergence * cell_avg_radius,
                                   msg="Incorrect cell radii produced by Epithelium.create_cell_sheet.")

    def test_create_cell_sheet_rerun(self):
        """Ensures that an Epithelium can correctly populate its cell with additional cells after init."""
        cell_quantity = 1
        cell_radius_divergence = .1
        cell_avg_radius = 1
        epithelium = Epithelium(cell_quantity, cell_radius_divergence, cell_avg_radius)

        # set the new number of cells
        new_cell_quantity = 19
        epithelium.cell_quantity = new_cell_quantity
        epithelium.create_cell_sheet()

        # ensure that there are the correct number of cells
        self.assertEqual(len(epithelium.cells), new_cell_quantity,
                         "Incorrect cell count after Epithelium.create_cell_sheet.")

        # ensure that the created cells match the input parameters
        for cell in epithelium.cells:
            self.assertAlmostEqual(cell.radius, cell_avg_radius, delta=cell_radius_divergence * cell_avg_radius,
                                   msg="Incorrect cell radii produced by Epithelium.create_cell_sheet.")

    def test_neighboring_cells(self):
        """Ensures that Epithelium.neighboring_cells returns the correct neighbors."""
        cell_quantity = 19
        cell_radius_divergence = 0
        cell_avg_radius = 1
        epithelium = Epithelium(cell_quantity, cell_radius_divergence, cell_avg_radius)

        neighbor_radius_count = 4
        for input_cell in epithelium.cells:
            # find cells within distance
            neighbor_cells = []
            for output_cell in epithelium.cells:
                if output_cell is not input_cell:
                    if distance((output_cell.position_x,
                                 output_cell.position_y,
                                 output_cell.position_z),
                                (input_cell.position_x,
                                 input_cell.position_y,
                                 input_cell.position_z)) < cell_avg_radius * neighbor_radius_count:
                        neighbor_cells.append(output_cell)

            calculated_neighbor_cells = list(epithelium.neighboring_cells(input_cell, neighbor_radius_count))
            self.assertListEqual(neighbor_cells,
                                 calculated_neighbor_cells,
                                 "incorrect neighbors returned from Epithelium.neighboring_cells.")

