import wx
from epithelium_backend.Cell import Cell


class SnapshotDisplay(object):
    """Instantly displays the current state of an epithelium in 2D"""
    
    def __init__(self, title: str = "Default", size: tuple = (300, 300), cells: list = None) -> None:
        """
        Creates a visual representation of a list of cells in a single moment in time
        :param title: The name of this snapshot and its window
        :param size: the dimensions of the window
        :param cells: the cells to display
        """

        self.cells = cells  # type: list

        # ensure that cells always stores a valid list.
        # cant just use valid list as default param because of python quirk
        if cells is None:
            self.cells = []

        # draw
        self.app = wx.App()  # type: wx.App
        self.frame = wx.Frame(None, title="Snapshot: "+title, size=size)  # type: wx.Frame
        self.frame.Bind(wx.EVT_PAINT, self.on_paint)
        self.frame.Show(True)
        self.app.MainLoop()

    def on_paint(self, e):
        """
        callback bound to the wx.EVT_PAINT event.
        Draws all cells.
        :param e: event information
        :return: None
        """

        dc = wx.PaintDC(self.frame)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))

        for cell in self.cells:
            dc.DrawCircle(cell.position[0], cell.position[1], cell.radius)
