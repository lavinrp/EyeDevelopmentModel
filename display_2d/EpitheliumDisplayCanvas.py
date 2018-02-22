

import wx
from wx import glcanvas
import ModernGL
from pyrr import matrix44
import numpy
from display_2d.EpitheliumGlTranslator import format_epithelium_for_gl
from display_2d.EpitheliumGlTranslator import gl_bytes_per_cell
from display_2d.Simple2dGlProgram import Simple2dGlProgram


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        glcanvas.GLCanvas.__init__(self, parent, size=(parent.GetSize()), name='epithelium_display_canvas')
        # GL
        self.wx_context = None  # type:  glcanvas.GLContext
        self.context = None  # type: ModernGL.Context
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 0.01  # type: float
        self.__scale_matrix = matrix44.create_from_scale((self.__scale,
                                                          self.__scale,
                                                          self.__scale))  # type: numpy.ndarray
        self.__translate_matrix = matrix44.create_from_translation((self.__camera_x,
                                                                    self.__camera_y,
                                                                    0))  # type: numpy.ndarray
        self.__gl_initialized = False  # type: bool
        self.empty_circle_gl_program = Simple2dGlProgram()  # type: Simple2dGlProgram
        self.empty_circle_gl_program.reserved_object_count = 1000
        self.empty_circle_gl_program.reserved_object_bytes = gl_bytes_per_cell
        self.filled_circle_gl_program = Simple2dGlProgram()  # type: Simple2dGlProgram
        self.filled_circle_gl_program.reserved_object_count = 500
        self.filled_circle_gl_program.reserved_object_bytes = gl_bytes_per_cell

        # event handling
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.__panning = False  # type: bool
        self.__last_mouse_position = [0, 0]  # type: list

    def on_paint(self, e: wx.PaintEvent = None):
        """Callback executed when an instance of this widget repaints

        (re)initializes all OpenGL settings and draws the epithelium."""

        if not self.__gl_initialized:
            self._init_gl()

        # prepare context for rendering
        self.SetCurrent(self.wx_context)
        self.context.clear(0.9, 0.9, 0.9)

        self._draw_epithelium()

        if e:
            e.Skip(False)

    def on_size(self, e: wx.SizeEvent):
        """Event handler for resizing Does not consume the size event.
        Flags on_paint to fix aspect ratio"""
        size = self.GetParent().GetSize()
        self.SetSize(size)
        if self.context:
            self.context.viewport = (0, 0, size.width, size.height)

        #if self.__empty_circle_program:
        #    projection = matrix44.create_perspective_projection_from_bounds(0,
        #                                                                    self.GetSize().width,
        #                                                                    0,
        #                                                                    self.GetSize().height,
        #                                                                    0,
        #                                                                    1)

            #self.__program.uniforms["projection"].value = tuple(projection.flatten())

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
                self.pan_camera(self.__last_mouse_position[0] - current_mouse_position[0],
                                -(self.__last_mouse_position[1] - current_mouse_position[1]))

        # scroll wheel
        wheel_rotation = event.GetWheelRotation()
        if wheel_rotation > 0:
            self.set_scale(1.1)
        elif wheel_rotation < 0:
            self.set_scale(0.9)

        # update mouse position
        self.__last_mouse_position = current_mouse_position

    def pan_camera(self, delta_x: float, delta_y: float) -> None:
        """Pan the camera by the specified deltas
        :param delta_x: change in the x of the camera
        :param delta_y: change in the y of the camera
        """

        distance_modifier = 0.2  # type: float

        self.__camera_x -= delta_x * distance_modifier
        self.__camera_y -= delta_y * distance_modifier

        self.__translate_matrix = matrix44.create_from_translation((self.__camera_x,
                                                                    self.__camera_y,
                                                                    0))  # type: numpy.ndarray
        self.on_paint()

    def set_scale(self, relative_scale: float) -> None:
        """
        Scales the displayed epithelium.
        :param relative_scale: The scale of the new display represented as a fraction of the previous scale
        Example: 1.1 with an original scale of 2.0 will produce a new scale of 2.2.
        :return:
        """
        self.__scale *= relative_scale
        self.__scale_matrix = matrix44.create_from_scale((self.__scale,
                                                          self.__scale,
                                                          self.__scale))  # type: numpy.ndarray
        self.on_paint()

    def _draw_epithelium(self) -> None:
        """
        Draws the epithelium stored by this widgets parent.
        Draws the epithelium to a pre-selected, pre-cleared, GL context.
        :return:
        """

        # update cell positions
        cell_data = format_epithelium_for_gl(self.epithelium)  # type: numpy.ndarray
        self.empty_circle_gl_program.update_vertex_objects(cell_data[0])
        self.filled_circle_gl_program.update_vertex_objects(cell_data[1])

        # update the model (zoom / pan)
        model = matrix44.multiply(self.__translate_matrix, self.__scale_matrix)  # type: numpy.ndarray
        model_tuple = tuple(model.flatten())
        self.empty_circle_gl_program.program.uniforms["model"].value = model_tuple
        self.filled_circle_gl_program.program.uniforms["model"].value = model_tuple

        # TODO: use projection matrix to fix stretching on window resize
        projection = matrix44.create_perspective_projection_from_bounds(0,
                                                                        self.GetSize().width,
                                                                        0,
                                                                        self.GetSize().height,
                                                                        0,
                                                                        1)
        # self.__program.uniforms["projection"].value = tuple(projection.flatten())

        self.empty_circle_gl_program.vao.render(mode=ModernGL.POINTS)
        self.filled_circle_gl_program.vao.render(mode=ModernGL.POINTS)

        self.SwapBuffers()

    def _init_gl(self) -> None:
        """
        Initializes all internal OpenGL elements (Shader Program, gl context, etc...).
        Sets __gl_initialized to true.
        """

        # context setup
        self.wx_context = glcanvas.GLContext(self)
        self.SetCurrent(self.wx_context)
        self.context = ModernGL.create_context()

        # empty circle program setup
        self.empty_circle_gl_program.context = self.context
        vertex_shader_path = r"display_2d/shaders/CircleGenerator.vert"
        geometry_shader_path = r"display_2d/shaders/EmptyCircleGenerator.geom"
        fragment_shader_path = r"display_2d/shaders/CircleGenerator.frag"
        self.empty_circle_gl_program.create_program(vertex_shader_path, geometry_shader_path, fragment_shader_path)
        self.empty_circle_gl_program.init_vertex_objects('2f3f1f', ['vert', 'vert_color', 'vert_radius'])

        # filled circle program setup
        self.filled_circle_gl_program.context = self.context
        vertex_shader_path = r"display_2d/shaders/CircleGenerator.vert"
        geometry_shader_path = r"display_2d/shaders/FilledCircleGenerator.geom"
        fragment_shader_path = r"display_2d/shaders/CircleGenerator.frag"
        self.filled_circle_gl_program.create_program(vertex_shader_path, geometry_shader_path, fragment_shader_path)
        self.filled_circle_gl_program.init_vertex_objects('2f3f1f', ['vert', 'vert_color', 'vert_radius'])

        self.__gl_initialized = True

    @property
    def epithelium(self):
        return self.GetParent().epithelium
