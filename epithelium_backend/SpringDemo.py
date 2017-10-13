from display_2d.SnapshotDisplay import SnapshotDisplay
from epithelium_backend.Cell import Cell
from epithelium_backend.SpringSimulator import decompact
import random as random
import wx

random.seed(58293)
# Generate 100 random cells about the origin with radii between 0.1 and 0.35
cells = [Cell((random.random(), random.random(), 0),
            (10 + (random.random() * 100))/2)
         for i in range(0, 100)]

# Plot the cells as they were spawned
snap = SnapshotDisplay("epithelium demo before ", (500, 500), cells)
# Decompact 250 times with kind of arbitrary parameters
decompact(cells, iterations=250, spring_constant=8, escape=1.05, dt=0.1)
# Plot the cells after being decompacted
snap2 = SnapshotDisplay("epithelium demo after", (500, 500), cells)
