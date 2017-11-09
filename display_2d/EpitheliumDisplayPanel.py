import wx
from wx import glcanvas

from OpenGL.GL import *

from epithelium_backend.Epithelium import Epithelium


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent):
        # TODO: correctly set the size of EpitheliumDisplayCanvas
        glcanvas.GLCanvas.__init__(self, parent, size=(10000, 10000), name='epithelium_display_canvas')
        self.context = None  # type: glcanvas.GLContext

        self.Bind(wx.EVT_PAINT, self.on_draw)

    def on_draw(self, e):
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0.1, 0.15, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.SwapBuffers()


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, parent, a, b, c, d) -> None:

        # init the panel
        super().__init__(parent, a, b, c, d)

        # create gl canvas
        self.gl_canvas = EpitheliumDisplayCanvas(self)

        # create default epithelium
        self.epithelium = Epithelium(5)  # type: Epithelium
