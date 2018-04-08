import unittest

from epithelium_backend.Cell import Cell
from epithelium_backend.CellCollisionHandler import distance
from epithelium_backend.CellCollisionHandler import CellCollisionHandler

class CellCollisionHandlerTester(unittest.TestCase):

    def test_resizing(self):
        # The collision handler should resize itself when cells no
        # longer fit in its grid
        cells = [Cell((0,0,0), 1), Cell((1,1,0), 1)]
        handler = CellCollisionHandler(cells)
        center_bin = (handler.dimension*handler.dimension - 1)/2
        init_dimension = handler.dimension
        self.assertEqual(handler.center_x, 0.5, "The center is (0.5, 0.5)")
        self.assertEqual(handler.center_y, 0.5, "The center is (0.5, 0.5)")
        self.assertEqual(handler.bin(cells[0]), center_bin, "Cell 0 is in the center bin")
        self.assertEqual(handler.bin(cells[1]), center_bin, "Cell 1 is in the center bin")

        # Register a new cell that fits within the grid
        cell_2 = Cell((0.5, 0.5, 0), 1)
        handler.register(cell_2)
        self.assertEqual(handler.dimension, init_dimension, "The handler didn't grow.")
        self.assertEqual(handler.bin(cell_2), center_bin, "Cell 2 is in the center bin.")

        # Register a cell that doesn't fit within the grid
        cell_3 = Cell((5, 5, 0), 1)
        handler.register(cell_3)
        self.assertTrue(handler.dimension > init_dimension, "The handler grew.")
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

    def test_decompact(self):
        cells = [Cell((0,0,0), 1),
                 Cell((1,1,0), 1),
                 Cell((1,0,0), 1),
                 Cell((0,1,0), 1)]
        handler = CellCollisionHandler(cells)

        def get_pairwise_distances():
            ds = []
            for i in range(0, len(cells)):
                for j in range(i+1, len(cells)):
                    c1 = cells[i]
                    c2 = cells[j]
                    ds.append(distance((c1.position_x, c1.position_y, 0),
                                       (c2.position_x, c2.position_y, 0)))
            return ds

        old_pairwise_distances = get_pairwise_distances()
        new_pairwise_distances = old_pairwise_distances
        # Every time we decompact, the cells should move farther apart.
        for i in range(0,10):
            handler.decompact()
            new_pairwise_distances = get_pairwise_distances()
            for new_dist, old_dist in zip(new_pairwise_distances, old_pairwise_distances):
                self.assertTrue(new_dist > old_dist, "The cells moved farther apart.")
            old_pairwise_distances = new_pairwise_distances
