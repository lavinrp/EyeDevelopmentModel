import wx
from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *

from display_2d.GlDrawingPrimitives import draw_circle
from gl_support.ShaderGenerator import ShaderGenerator
from ctypes import c_void_p


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        glcanvas.GLCanvas.__init__(self, parent, size=(parent.GetSize()), name='epithelium_display_canvas')

        # GL
        self.context = None  # type: glcanvas.GLContext
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 0.01  # type: float
        self.__gl_initialized = False  # type: bool

        # shader
        self.shader_program = None
        self.vertexPositions = [
            0.0, 1.0,
            1.0, 0.0,
            0.0, -1.0,
            -1.0, 0.0,
        ]

        # event handling
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.__panning = False  # type: bool
        self.__last_mouse_position = [0, 0]  # type: list

    def on_paint(self, e: wx.PaintEvent):
        """Callback executed when an instance of this widget repaints

        (re)initializes all OpenGL settings and draws the epithelium."""

        if not self.__gl_initialized:
            self._initialize_buffers()
            shader_generator = ShaderGenerator(r"display_2d/shaders")
            self.shader_program = shader_generator.create_program("SimplePoints.vert",
                                                                  "SimpleColor.frag")
            self.__gl_initialized = True

            # context setup
            # self.context = glcanvas.GLContext(self)
            self.SetCurrent(self.context)

            # gl settings
            glClearColor(.9, .9, .9, 1)
            glLoadIdentity()

        # display epithelium BRIAN TESTING begin _draw_epithelium

        # glUseProgram(self.shader_program)

        """
        Draws the epithelium stored by this widgets parent.
        Draws the epithelium to a pre-selected GL context.
        :return:
        """

        test = glValidateProgram(self.shader_program)
        glUseProgram(self.shader_program)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, False, 0, c_void_p(0))

        glDrawArrays(GL_TRIANGLES, 0, 4)
        # shader_attr_position = glGetAttribLocation(self.shader_program, "position")
        # shader_attr_color = glGetAttribLocation(self.shader_program, "color")
        glDisableVertexAttribArray(0)
        glUseProgram(0)

        self.SwapBuffers()

        # end of _drawepithelium
        # self._draw_epithelium()

    def on_size(self, e: wx.SizeEvent):
        """Event handler for resizing Does not consume the size event.
        Flags on_paint to fix aspect ratio"""
        self.SetSize(self.GetParent().GetSize())
        e.Skip()

    def on_mouse_events(self, event: wx.MouseEvent):
        """Handle all mouse event logic.
        This includes: camera panning
        :param event: the mouse event to handle
        """

        # get mouse position
        current_mouse_position = [event.GetX(), event.GetY()]

        # left mouse button down
        if event.ButtonDown(wx.MOUSE_BTN_LEFT):
            self.__panning = True

        # left mouse button up
        if event.ButtonUp(wx.MOUSE_BTN_LEFT):
            self.__panning = False

        # mouse drag
        if event.Dragging():

            # panning
            if self.__panning:
                self._pan_camera(self.__last_mouse_position[0] - current_mouse_position[0],
                                 -(self.__last_mouse_position[1] - current_mouse_position[1]))

        # scroll wheel
        wheel_rotation = event.GetWheelRotation()
        if wheel_rotation > 0:
            self._set_scale(1.1)
        elif wheel_rotation < 0:
            self._set_scale(0.9)

        # update mouse position
        self.__last_mouse_position = current_mouse_position

    def _pan_camera(self, delta_x: float, delta_y: float) -> None:
        """Pan the camera by the specified deltas
        :param delta_x: change in the x of the camera
        :param delta_y: change in the y of the camera
        """

        distance_modifier = 0.01  # type: float

        self.__camera_x += delta_x * distance_modifier
        self.__camera_y += delta_y * distance_modifier
        self.on_paint(None)

    def _set_scale(self, relative_scale: float) -> None:
        """
        Scales the displayed epithelium.
        :param relative_scale: The new scale to display the epithelium
        relative to the current scale. Example: 1.1 will produce a zooming effect
        resulting in a 10% greater scale
        :return:
        """
        self.__scale *= relative_scale
        self.on_paint(None)

    def _draw_epithelium(self) -> None:
        """
        Draws the epithelium stored by this widgets parent.
        Draws the epithelium to a pre-selected GL context.
        :return:
        """

        test = glValidateProgram(self.shader_program)
        glUseProgram(self.shader_program)

        # shader_attr_position = glGetAttribLocation(self.shader_program, "position")
        # shader_attr_color = glGetAttribLocation(self.shader_program, "color")
        self.SwapBuffers()

    def _initialize_buffers(self):

        # context setup
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        array_type = (GLfloat * len(self.vertexPositions))
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertexPositions) * 4,
                     array_type(*self.vertexPositions),
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)
        glEnableVertexAttribArray(0)
