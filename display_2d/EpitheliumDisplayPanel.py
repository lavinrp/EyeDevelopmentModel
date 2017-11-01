import wx
from epithelium_backend.Epithelium import Epithelium


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, parent, a, b, c, d) -> None:

        # init the panel
        super().__init__(parent, a, b, c, d)

        # bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

        # create default epithelium
        self.epithelium = Epithelium(5)  # type: Epithelium

        # init drawing vars
        self.zoom = 1  # type: float
        self.position_x = 0  # type: float
        self.position_y = 0  # type: float

    def on_mouse_wheel(self, e: wx.MouseEvent) -> None:
        """
        zooms the window based on mouse scrolling
        :param e: event information
        :return: None
        """

        min_zoom = 0.001

        self.zoom += e.GetWheelRotation()/e.GetWheelDelta() * 0.1
        if self.zoom <= min_zoom:
            self.zoom = min_zoom


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
            dc.DrawCircle((cell.position[0] + self.position_x) * self.zoom,
                          (cell.position[1] + self.position_y) * self.zoom
                          , cell.radius * self.zoom)
