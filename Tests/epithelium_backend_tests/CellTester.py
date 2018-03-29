import unittest
import math

from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.CellCollisionHandler import CellCollisionHandler


class CellTester(unittest.TestCase):
    """
    Test properties and behaviors of epithelium_backend.Cell
    """

    def test_init(self):
        x = 1
        y = 2
        z = 0
        radius = 2
        photoreceptor_type = PhotoreceptorType.R8
        support_specializations = {"test"}
        cell = Cell((x, y, z), radius, photoreceptor_type, support_specializations)

        self.assertEqual(cell.position_x, x, "Incorrect cell position assigned by Cell.__init__")
        self.assertEqual(cell.position_y, y, "Incorrect cell position assigned by Cell.__init__")
        self.assertEqual(cell.position_z, z, "Incorrect cell position assigned by Cell.__init__")
        self.assertEqual(cell.radius, radius, "Incorrect cell radius assigned by Cell.__init__")
        self.assertEqual(cell.photoreceptor_type, photoreceptor_type,
                         "Incorrect photoreceptor type assigned by Cell.__init__")
        self.assertEqual(cell.support_specializations, support_specializations,
                         "Incorrect support specialization assigned by Cell.__init__")

    def test_divide(self):
        # init parent
        x = 1
        y = 2
        z = 0
        radius = 2
        photoreceptor_type = PhotoreceptorType.NOT_RECEPTOR
        support_specializations = set()
        cell = Cell((x, y, z), radius, photoreceptor_type, support_specializations)
        cell_collision_handler = CellCollisionHandler([cell])

        # divide
        child = cell.divide(cell_collision_handler)

        # check radii
        self.assertEqual(cell.radius, radius/2, "Incorrect radii after cell.divide")
        self.assertEqual(child.radius, radius/2, "Incorrect radii after cell.divide")

        # check position
        cell_dist = math.hypot(cell.position_x - child.position_x, cell.position_y - child.position_y)
        # cells should now have a cell radius of radius/2. The cells centers should be two of this distance apart.
        self.assertAlmostEqual(cell_dist, 2*(radius/2), msg="Incorrect cell spacing after cell.divide", delta=.01)

    def test_grow_cell(self):
        # init parent
        x = 1
        y = 2
        z = 0
        radius = 2
        photoreceptor_type = PhotoreceptorType.NOT_RECEPTOR
        support_specializations = set()
        cell = Cell((x, y, z), radius, photoreceptor_type, support_specializations)

        growth_amount = 0.6
        cell.grow_cell(growth_amount)

        self.assertEqual(cell.radius, radius+growth_amount, "Cell.grow_cell incorrectly changes cell size")
