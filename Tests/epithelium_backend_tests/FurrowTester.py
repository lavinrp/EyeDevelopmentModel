import unittest
import math

from epithelium_backend.Epithelium import Epithelium

from epithelium_backend.FurrowEvent import FurrowEvent
from epithelium_backend.Furrow import Furrow


class TestEventFunctor(FurrowEvent):
    """
    Fake FurrowEvent used for testing furrows.
    """
    def __init__(self):
        """init the test functor"""
        self.call_count = 0
        distance_from_furrow = 10
        FurrowEvent.__init__(self, distance_from_furrow, dict(), self.run_func)
        self.field_types = {}
        self.epithelium = None
        self.cells = []

    def run_func(self, field_types, epithelium, cells):
        """function called whenever this functor is called"""
        self.epithelium = epithelium
        self.field_types = field_types
        self.cells = cells
        self.call_count += 1


class FurrowTester(unittest.TestCase):

    def test_init(self):
        pos = 10
        velocity = 0
        events = []

        furrow = Furrow(pos, velocity, events)  # type: Furrow

        self.assertListEqual(furrow.events, events, "events incorrectly set in Furrow.__init__.")
        self.assertEqual(furrow.velocity, velocity, "velocity incorrectly set in Furrow.__init__.")
        self.assertEqual(furrow.position, pos, "position incorrectly set in Furrow.__init__.")
        self.assertEqual(furrow.last_position, math.inf, "last_position not initialized to inf in Furrow.__init__.")

    def test_advance(self):
        velocity = 10
        initial_position = 20
        advance_distance = 5
        furrow = Furrow(position=initial_position, velocity=velocity)

        furrow.advance(advance_distance)

        self.assertEqual(furrow.position, initial_position - advance_distance,
                         "Furrow incorrectly moved during Furrow.advance")

        self.assertEqual(furrow.last_position, initial_position, "last_position incorrectly updated by Furrow.advance")

    def test_update(self):

        # init furrow
        pos = 10
        velocity = 10
        test_functor = TestEventFunctor()
        events = [test_functor]
        furrow = Furrow(pos, velocity, events)  # type: Furrow

        # init epithelium
        cell_quantity = 10
        epithelium = Epithelium(cell_quantity)

        # update the epithelium
        furrow.update(epithelium)

        # check results
        self.assertEqual(furrow.position, pos - velocity, "Incorrect position set by Furrow.update")
        self.assertEqual(test_functor.epithelium, epithelium, "Incorrect epithelium updated in Furrow.update")
        self.assertEqual(test_functor.call_count, 1, "FurrowEvent called incorrect number of times in Furrow.update")
        self.assertEqual(furrow.last_position, pos, "last_position not initialized to inf in Furrow.update")


