import unittest
import numpy as np

from epithelium_backend.Cell import Cell
from epithelium_backend.CellCollisionHandler import distance
from epithelium_backend.CellCollisionHandler import CellCollisionHandler
from epithelium_backend.CellCollisionHandler import create_cell_grid
from quick_change.CellEvents import UpdateCellPosition


def get_pairwise_distances(cells: list):
    distances = []
    for i in range(0, len(cells)):
        for j in range(i + 1, len(cells)):
            c1 = cells[i]
            c2 = cells[j]
            distances.append(distance((c1.position_x, c1.position_y, 0),
                               (c2.position_x, c2.position_y, 0)))
    return distances


class CellCollisionHandlerTester(unittest.TestCase):

    def test_resizing(self):
        # The collision handler should resize itself when cells no
        # longer fit in its grid
        cells = [Cell((0,0,0), 1), Cell((1,1,0), 1)]
        handler = CellCollisionHandler(cells)
        initial_dimension = handler.dimension

        # Register a new cell that fits within the grid
        cell_2 = Cell((0.5, 0.5, 0), 1)
        handler.register(cell_2)
        self.assertEqual(handler.dimension, initial_dimension, "The handler didn't grow.")

        # Register a cell that doesn't fit within the grid
        cell_3 = Cell((5, 5, 0), 1)
        handler.register(cell_3)
        self.assertTrue(handler.dimension > initial_dimension, "The handler grew.")
        self.assertEqual(handler.center_x, 1.625, "The center was adjusted.")
        self.assertEqual(handler.center_y, 1.625, "The center was adjusted.")

    def test_push_pull(self):
        def push_pull(position_1, position_2):
            cell1 = Cell(position_1, 1)
            cell2 = Cell(position_2, 1)
            initial_distance = distance(position_1, position_2)
            cells = [cell1, cell2]
            handler = CellCollisionHandler(cells)
            handler.push_pull(cell1, cell2)
            position_updater = UpdateCellPosition()  # type: UpdateCellPosition
            for cell in cells:
                position_updater(cell)
            current_distance = distance((cell1.position_x, cell1.position_y, 0),
                                        (cell2.position_x, cell2.position_y, 0))
            return initial_distance, current_distance

        init_dist, new_dist = push_pull((0,0,0), (0,0,0))
        self.assertTrue(new_dist > init_dist,
                        "Cells on top of each other push each other apart.")

        init_dist, new_dist = push_pull((0,0,0), (0.5, 0, 0))
        self.assertTrue(new_dist > init_dist,
                        "Grossly overlapping cells push each other apart.")

        # see the allow_overlap parameter
        init_dist, new_dist = push_pull((0, 0, 0), (1.98, 0, 0))
        self.assertTrue(new_dist < init_dist,
                        "Very slightly overlapping cells pull each other together")

        # see the force_escape parameter
        init_dist, new_dist = push_pull((0, 0, 0), (2.02, 0, 0))
        self.assertTrue(new_dist < init_dist,
                        "Slightly not-touching cells pull each other together")

        init_dist, new_dist = push_pull((0, 0, 0), (5, 0, 0))
        self.assertTrue(new_dist == init_dist,
                        "Far away cells don't affect each other.")

        # Forces scale linearly with distance
        init_dist_close, new_dist_close = push_pull((0,0,0), (0.5, 0, 0))
        init_dist_far, new_dist_far = push_pull((0,0,0), (1, 0, 0))
        self.assertTrue(new_dist_close - init_dist_close > new_dist_far - init_dist_far,
                        "Push/pull forces are greater when cells are closer together.")

    def test_decompact_line_coincident_cells(self):
        cells = [Cell((0, 0, 0), 1),
                 Cell((0, 0, 0), 1)]
        handler = CellCollisionHandler(cells)

        old_pairwise_distances = get_pairwise_distances(cells)

        # Every time we decompact, the cells should move farther apart.
        handler.decompact()
        new_pairwise_distances = get_pairwise_distances(cells)
        for new_dist, old_dist in zip(new_pairwise_distances, old_pairwise_distances):
            self.assertTrue(new_dist > old_dist, "The cells moved farther apart.")

    def test_decompact_2cell(self):
        cells = [Cell((0, 0, 0), 1),
                 Cell((0, 1, 0), 1)]
        handler = CellCollisionHandler(cells)

        old_pairwise_distances = get_pairwise_distances(cells)

        # Every time we decompact, the cells should move farther apart.
        handler.decompact()
        new_pairwise_distances = get_pairwise_distances(cells)
        for new_dist, old_dist in zip(new_pairwise_distances, old_pairwise_distances):
            self.assertTrue(new_dist > old_dist, "The cells moved farther apart.")

    def test_decompact_line_3cell(self):
        cells = [Cell((0, 0, 0), 1),
                 Cell((0, 1, 0), 1),
                 Cell((0, 2, 0), 1),
                 ]
        handler = CellCollisionHandler(cells)

        old_pairwise_distances = get_pairwise_distances(cells)

        # Every time we decompact, the cells should move farther apart.
        handler.decompact()
        new_pairwise_distances = get_pairwise_distances(cells)
        for new_dist, old_dist in zip(new_pairwise_distances, old_pairwise_distances):
            self.assertTrue(new_dist > old_dist, "The cells moved farther apart.")

    def test_decompact_triangle_3cell(self):
        cells = [Cell((0, 0, 0), 1),
                 Cell((1, 0, 0), 1),
                 Cell((.5, 0.866, 0), 1),
                 ]
        handler = CellCollisionHandler(cells)

        old_pairwise_distances = get_pairwise_distances(cells)

        # Every time we decompact, the cells should move farther apart.
        handler.decompact()
        new_pairwise_distances = get_pairwise_distances(cells)
        for new_dist, old_dist in zip(new_pairwise_distances, old_pairwise_distances):
            self.assertTrue(new_dist > old_dist, "The cells moved farther apart.")

    def test_create_cell_grid_same_size_cells_no_children_grid_dimensions(self):
        cell_radius = 10
        cells = [
            Cell((0, 0, 0), cell_radius),
            Cell((20, 0, 0), cell_radius),
            Cell((40, 0, 0), cell_radius),
            Cell((60, 0, 0), cell_radius),
            Cell((80, 0, 0), cell_radius),
            Cell((20, 20, 0), cell_radius),
            Cell((40, 20, 0), cell_radius),
            Cell((60, 20, 0), cell_radius),
            Cell((80, 20, 0), cell_radius),
            Cell((0, 20, 0), cell_radius)
        ]

        # create the grid
        grid = create_cell_grid(cells)  # type: np.ndarray

        # check the shape of the grid
        grid_shape = grid.shape
        self.assertEqual((5,2), grid_shape, "The grid was created with incorrect dimensions.")

    def test_create_cell_grid_same_size_cells_no_children_cell_positions(self):
        cell_radius = 10
        cells = [
            Cell((0, 0, 0), cell_radius),
            Cell((20, 0, 0), cell_radius),
            Cell((40, 0, 0), cell_radius),
            Cell((60, 0, 0), cell_radius),
            Cell((80, 0, 0), cell_radius),
            Cell((0, 20, 0), cell_radius),
            Cell((20, 20, 0), cell_radius),
            Cell((40, 20, 0), cell_radius),
            Cell((60, 20, 0), cell_radius),
            Cell((80, 20, 0), cell_radius)
        ]

        # create the grid
        grid = create_cell_grid(cells)  # type: np.ndarray

        # assert that all the bins have exactly one cell in them
        self.assertEqual(len(grid[0][0]), 1)
        self.assertEqual(len(grid[1][0]), 1)
        self.assertEqual(len(grid[2][0]), 1)
        self.assertEqual(len(grid[3][0]), 1)
        self.assertEqual(len(grid[4][0]), 1)
        self.assertEqual(len(grid[0][1]), 1)
        self.assertEqual(len(grid[1][1]), 1)
        self.assertEqual(len(grid[2][1]), 1)
        self.assertEqual(len(grid[3][1]), 1)
        self.assertEqual(len(grid[4][1]), 1)

        # assert that the cells ended up in the correct bin
        self.assertIs(cells[0], grid[0][0][0])
        self.assertIs(cells[1], grid[1][0][0])
        self.assertIs(cells[2], grid[2][0][0])
        self.assertIs(cells[3], grid[3][0][0])
        self.assertIs(cells[4], grid[4][0][0])
        self.assertIs(cells[5], grid[0][1][0])
        self.assertIs(cells[6], grid[1][1][0])
        self.assertIs(cells[7], grid[2][1][0])
        self.assertIs(cells[8], grid[3][1][0])
        self.assertIs(cells[9], grid[4][1][0])

    def test_create_cell_grid_same_size_cells_no_children_cell_positions_with_gaps_between_cells(self):
        cell_radius = 10
        cells = [
            Cell((0, 0, 0), cell_radius),
            Cell((40, 0, 0), cell_radius),
            Cell((80, 0, 0), cell_radius),
            Cell((0, 40, 0), cell_radius),
            Cell((40, 40, 0), cell_radius),
            Cell((80, 40, 0), cell_radius)
        ]

        # create the grid
        grid = create_cell_grid(cells)  # type: np.ndarray

        # assert that the correct bins have cells in them
        self.assertEqual(len(grid[0][0]), 1)
        self.assertEqual(len(grid[1][0]), 0)
        self.assertEqual(len(grid[2][0]), 1)
        self.assertEqual(len(grid[3][0]), 0)
        self.assertEqual(len(grid[4][0]), 1)
        self.assertEqual(len(grid[0][1]), 0)
        self.assertEqual(len(grid[1][1]), 0)
        self.assertEqual(len(grid[2][1]), 0)
        self.assertEqual(len(grid[3][1]), 0)
        self.assertEqual(len(grid[4][1]), 0)
        self.assertEqual(len(grid[0][2]), 1)
        self.assertEqual(len(grid[1][2]), 0)
        self.assertEqual(len(grid[2][2]), 1)
        self.assertEqual(len(grid[3][2]), 0)
        self.assertEqual(len(grid[4][2]), 1)

        # assert that the cells ended up in the correct bin
        self.assertIs(cells[0], grid[0][0][0])
        self.assertIs(cells[1], grid[2][0][0])
        self.assertIs(cells[2], grid[4][0][0])
        self.assertIs(cells[3], grid[0][2][0])
        self.assertIs(cells[4], grid[2][2][0])
        self.assertIs(cells[5], grid[4][2][0])

    def test_minimum_bin_size_is_max_cell_size(self):
        """
        Bin sizes cannot be smaller than the size of hte largest cell without
        incorrect collision calsucations
        """

        # fill a collision handler with cells
        big_cell_size = 100
        cells = [
            Cell((1, 1, 0), 1),
            Cell((1, 70, 0), big_cell_size),
            Cell((1, 2, 0), 1),
            Cell((1, 3, 0), 1)
        ]
        collision_handler = CellCollisionHandler(cells)
        collision_handler.fill_grid()

        # ensure that the the cells
        self.assertGreaterEqual(
            collision_handler.box_size,
            big_cell_size,
            "The collision handler box size is smaller than the largest cell."
        )

    def test_decompact_with_big_cell(self):
        """
        Ensure that cells get pushed and pulled even if one cell is
        significantly larger than the rest
        """

        # fill a collision handler with cells
        big_cell_size = 100
        big_cell_position = (0, 0, 0)
        big_cell = Cell(big_cell_position, big_cell_size)
        cell_positions = [
            (-90, 0, 0),
            (90, 0, 0),
            (90, 90, 0),
            big_cell_size
        ]
        cells = [
            Cell(cell_positions[0], 1),
            Cell(cell_positions[1], 1),
            Cell(cell_positions[2], 1),
            big_cell
        ]
        collision_handler = CellCollisionHandler(cells)
        collision_handler.decompact()

        # the cells were overlapping significantly ensure that they got moved
        for i in range(len(cells)):
            cell = cells[i]
            orig_cell_position = cell_positions[i]
            if cell is not big_cell:
                cell_position = (
                    cell.position_x,
                    cell.position_y,
                    cell.position_z
                )
                new_big_cell_position = (
                    big_cell.position_x,
                    big_cell.position_y,
                    big_cell.position_z
                )
                old_distance = distance(cell_positions[i], big_cell_position)
                new_distance = distance(cell_position, new_big_cell_position)
                self.assertGreater(new_distance, old_distance, "Overlapping cells were not moved")


