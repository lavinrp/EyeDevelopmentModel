import wx
from wx import BoxSizer
from wx import glcanvas


from epithelium_backend.Epithelium import Epithelium
from display_2d.EpitheliumDisplayCanvas import EpitheliumDisplayCanvas


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, parent, _id, pos, _size, style) -> None:

        # init the panel
        super().__init__(parent, _id, pos, parent.GetSize(), style)

        # create gl canvas
        self.gl_canvas = EpitheliumDisplayCanvas(self)  # type: glcanvas

        # create default epithelium
        self.epithelium = Epithelium(5)  # type: Epithelium
