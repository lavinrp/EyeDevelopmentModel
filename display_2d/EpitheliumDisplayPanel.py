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
        glcanvas.GLCanvas.__init__(self, parent, size=(500, 500), name='epithelium_display_canvas')
        self.context = None  # type: glcanvas.GLContext
        self.Bind(wx.EVT_PAINT, self.on_draw)
        # self.Bind(wx.EVT_MOUSE)
        self._gl_initialized = False

    def on_draw(self, e):
        # openGL setup
        if not self._gl_initialized:

            # context setup
            self.context = glcanvas.GLContext(self)
            self.SetCurrent(self.context)

            # gl settings
            glViewport(0, 0, 500, 500)
            glLoadIdentity()
            glClearColor(.9, .9, .9, 1)
            glMatrixMode(GL_PROJECTION)
            gluLookAt(0, 0, 1,
                      0, 0, 0,
                      0, 1, 0)
            glScalef(0.1, 0.1, 1)

            # finalize init
            self._gl_initialized = True

        # draw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        draw_circle((0, 0), 0.3, True, color=(0, 1, 0, 1))
        draw_circle((0.6, 0), 0.3, True, color=(0, 0, 1, 1))

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
