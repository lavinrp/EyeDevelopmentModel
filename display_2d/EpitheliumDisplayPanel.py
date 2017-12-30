import wx
from wx import glcanvas

from OpenGL.GL import *

import numpy

from gl_support.ShaderGenerator import ShaderGenerator
from epithelium_backend.Epithelium import Epithelium


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent):
        # TODO: correctly set the size of EpitheliumDisplayCanvas
        glcanvas.GLCanvas.__init__(self, parent, size=(10000, 10000), name='epithelium_display_canvas')
        self.context = None  # type: glcanvas.GLContext
        self.Bind(wx.EVT_PAINT, self.on_draw)
        self._shader = None
        self._gl_initialized = False  # type: bool
        self._vertex_buffer_object = None  # TODO: figure out the type of this
        self._vertex_shader_input_position = None
        # self._gl_translator =

    def on_draw(self, e):
        # openGL setup
        if not self._gl_initialized:

            # context setup
            self.context = glcanvas.GLContext(self)
            self.SetCurrent(self.context)

            # shader setup
            shader_generator = ShaderGenerator(r"./display_2d/shaders")
            self._shader = shader_generator.create_program()

            # vbo setup
            self._vertex_buffer_object = glGenBuffers(1)
            position = glGetAttribLocation(self._shader, "position")
            glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer_object)

            # misc setup
            glClearColor(0.1, 0.15, 0.1, 1.0)
            self._gl_initialized = True

        ##########################
        triangle = [-0.5, -0.5, 0.0,
                    0.5, -0.5, 0.0,
                    0.0, 0.5, 0.0]
        triangle = numpy.array(triangle, dtype=numpy.float32)
        #########################

        # pass data to shader
        glBufferData(GL_ARRAY_BUFFER, len(triangle) * 4, triangle, GL_STATIC_DRAW)
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position)
        glUseProgram(self._shader)

        # draw
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)
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
