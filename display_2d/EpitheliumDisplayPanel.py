import wx


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, *args, **kwargs):

        # init the panel
        super().__init__(args, kwargs)

        # bind the on paint event handler
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.epithelium = None


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

        #for cell in self.cells:
        #    dc.DrawCircle(cell.position[0], cell.position[1], cell.radius)