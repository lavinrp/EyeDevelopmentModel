

import wx
from wx import glcanvas
import ModernGL

import struct

from numpy import array


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        glcanvas.GLCanvas.__init__(self, parent, size=(parent.GetSize()), name='epithelium_display_canvas')

        # GL
        self.wx_context = None # type:  glcanvas.GLContext
        self.context = None  # type: ModernGL.Context
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 0.01  # type: float
        self.__gl_initialized = False  # type: bool
        self.vao = None

        # shader
        self.shader_program = None
        self.vertexPositions = [
            [0.0, 1.0, 0],
            [1.0, 0.0, 0],
            [0.0, -1.0, 0],
            [-1.0, 0.0, 0]
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
            self._init_gl()

        self.SetCurrent(self.wx_context)
        self.context.clear(0.9, 0.9, 0.9)
        self.vao.render()
        self.SwapBuffers()

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

        self.SwapBuffers()

    def _init_gl(self):
        # context setup
        self.wx_context = glcanvas.GLContext(self)
        self.SetCurrent(self.wx_context)
        self.context = ModernGL.create_context()

        vert = self.context.vertex_shader('''
            #version 330
            in vec2 vert;
            void main() {
                gl_Position = vec4(vert, 0.0, 1.0);
            }
        ''')

        frag = self.context.fragment_shader('''
            #version 330
            out vec4 color;
            void main() {
                color = vec4(0.30, 0.50, 1.00, 1.0);
            }
        ''')

        program = self.context.program([vert, frag])

        vbo = self.context.buffer(struct.pack('6f', 0.0, 0.8, -0.6, -0.8, 0.6, -0.8))
        self.vao = self.context.simple_vertex_array(program, vbo, ['vert'])

        self.__gl_initialized = True
