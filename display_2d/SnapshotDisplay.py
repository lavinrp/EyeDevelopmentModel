import wx
from epithelium_backend.Cell import Cell


class SnapshotDisplay(wx.Frame):
    """Instantly displays the current state of an epithelium in 2D"""
    
    def __init__(self, title: str = "Default", size: tuple[int, int] = (300, 300), cells: list[Cell] = []) -> None:
        """
        Creates a visual representation of a list of cells in a single moment in time
        :param title: The name of this snapshot and its window
        :param size: the dimensions of the window
        :param cells: the cells to display
        """
        super(SnapshotDisplay, self).__init__(None, title="Snapshot: "+title, size=size)

        self.cells = cells  # type: list[Cell]

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Show(True)

    def on_paint(self, e):
        """
        callback bound to the wx.EVT_PAINT event.
        Draws all cells.
        :param e: event information
        :return: None
        """

        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))

        for cell in self.cells:
            dc.DrawCircle(cell.position[0], cell.position[1], cell.radius)
