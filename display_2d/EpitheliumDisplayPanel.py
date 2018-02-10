import wx
from wx import glcanvas


from epithelium_backend.Epithelium import Epithelium
from display_2d.EpitheliumDisplayCanvas import EpitheliumDisplayCanvas


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, parent, _id, pos, _size, style) -> None:

        # init the panel
        super().__init__(parent, _id, pos, parent.GetSize(), style)

        # callbacks
        self.Bind(wx.EVT_SIZE, self.on_size)

        # create default epithelium
        self._epithelium = Epithelium(0)  # type: Epithelium

        # create gl canvas
        self.gl_canvas = EpitheliumDisplayCanvas(self)  # type: glcanvas

    @ property
    def epithelium(self):
        """returns a reference to the epithelium stored in this EpitheliumDisplayPanel."""
        return self._epithelium

    @ epithelium.setter
    def epithelium(self, value: Epithelium) -> None:
        """
        Sets the epithelium for this instance of EpitheliumDisplayPanel
        Forces the child EpitheliumDisplayCanvas to paint
        :param value: Reference to new epithelium.
        """
        self._epithelium = value
        if self.IsShownOnScreen():
            self.gl_canvas.on_paint(None)

    def on_size(self, e: wx.SizeEvent):
        """Event handler for resizing Does not consume the size event.
        Also invokes resize callback for child EpitheliumDisplayCanvas."""
        self.SetSize(self.GetParent().GetSize())
        self.gl_canvas.on_size(e)
        e.Skip()

