from display_2d.SnapshotDisplay import SnapshotDisplay
from epithelium_backend.Cell import Cell
from epithelium_backend.SpringSimulator import decompact
from epithelium_backend.Epithelium import Epithelium
import random as random
import wx

if __name__ == '__main__':

    random.seed(58293)
    # Generate 100 random cells about the origin with radii between 0.1 and 0.35

    testEpithelium = Epithelium(100)

