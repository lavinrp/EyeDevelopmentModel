import unittest

from epithelium_backend.FurrowEvent import FurrowEvent
from epithelium_backend.Epithelium import Epithelium


class RunFunctor(object):
    def __init__(self):
        self.call_count = 0
        self.field_types = None
        self.cells = None

    def __call__(self, field_types, epithelium, cells):
        self.call_count += 1
        self.field_types = field_types
        self.cells = cells


class FurrowEventTester(unittest.TestCase):
    """
    Test properties and behaviors of FurrowEvent
    """

    def test_init(self):
        distance_from_furrow = 10
        field_types = {}
        run = RunFunctor()
        furrow_event = FurrowEvent("test event", distance_from_furrow, field_types, run)

        self.assertEqual(distance_from_furrow, furrow_event.distance_from_furrow,
                         "Incorrect distance from furrow set in FurrowEvent.__init__")
        self.assertEqual(field_types, furrow_event.field_types, "Incorrect field types set in FurrowEvent.__init__")
        self.assertEqual(run, furrow_event.run, "Incorrect run function set in FurrowEvent.__init__")

    def test_call(self):
        distance_from_furrow = 10
        field_types = {"test": 1}
        cell_count = 10
        epithelium = Epithelium(cell_count)
        run = RunFunctor()
        furrow_event = FurrowEvent("Test Event", distance_from_furrow, field_types, run)
        furrow_event(10000, -1000, epithelium)

        self.assertEqual(run.call_count, 1, "Incorrect call count of run function in FurrowEvent.__call__")
        self.assertDictEqual(run.field_types, field_types, "Incorrect field types sent to FurrowEvent.run")

        # ensure that all cells in the epithelium were passed to the
        #  run function (b/c of how far the epithelium has moved)
        missing_cell = False
        for cell in epithelium.cells:
            if cell not in run.cells:
                missing_cell = True
        self.assertEqual(missing_cell, False, "Incorrect cells passed to run function in FurrowEvent.__call__")






