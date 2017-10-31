import wx
from epithelium_backend.Epithelium import Epithelium


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, *args, **kwargs) -> None:

        # init the panel
        super().__init__(args, kwargs)

        # bind the on paint event handler
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.epithelium = Epithelium(1000)

    def on_paint(self, e) -> None:
        """
        callback bound to the wx.EVT_PAINT event.
        Draws all cells.
        :param e: event information
        :return: None
        """

        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))

        for cell in self.epithelium.cells:
            dc.DrawCircle(cell.position[0], cell.position[1], cell.radius)
