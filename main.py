from epithelium_backend.Cell import Cell
from display_2d.SnapshotDisplay import SnapshotDisplay
import wx

app = wx.App()

cells = []

# this does weird stuff, but that is fine for the test
for i in range(1, 100):
    cells.append(Cell(((i % 10) * 40, (i/10) * 40, 0), 10))

SnapshotDisplay("test", (500, 500), cells)

app.MainLoop()