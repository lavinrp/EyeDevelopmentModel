import wx
from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

from epithelium_backend.Epithelium import Epithelium
from display_2d.GlDrawingPrimitives import draw_circle


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent):
        # TODO: correctly set the size of EpitheliumDisplayCanvas
        glcanvas.GLCanvas.__init__(self, parent, size=(500, 500), name='epithelium_display_canvas') # 10000
        self.context = None  # type: glcanvas.GLContext
        self.Bind(wx.EVT_PAINT, self.on_draw)
        self._gl_initialized = False

    def on_draw(self, e):
        # openGL setup
        if not self._gl_initialized:

            # context setup
            self.context = glcanvas.GLContext(self)
            self.SetCurrent(self.context)
            self._gl_initialized = True
            glClearColor(0.2, 0.3, 0.1, 0.5)

        # draw
        glClear(GL_COLOR_BUFFER_BIT)
        # glDrawArrays(GL_TRIANGLES, 0, 3)

        draw_circle((0, 0), 0.5, True, color=(0, 1, 0, 1))

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
