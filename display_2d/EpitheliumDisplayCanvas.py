

import wx
from wx import glcanvas
import ModernGL
from pyrr import matrix44
import numpy
from gl_support.EpitheliumGlTranslator import format_epithelium_for_gl
from epithelium_backend.PhotoreceptorType import PhotoreceptorType


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        glcanvas.GLCanvas.__init__(self, parent, size=(parent.GetSize()), name='epithelium_display_canvas')

        # GL
        self.wx_context = None  # type:  glcanvas.GLContext
        self.context = None  # type: ModernGL.Context
        self.__program = None  # type: ModernGL.Program
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
        self.vao = None  # type: ModernGL.VertexArray
        self.vbo = None  # type: ModernGL.Buffer
        # used for optimizing vbo and vao creation
        self._gl_reserved_cell_count = 1000  # type: int

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

        if self.__program:
            projection = matrix44.create_perspective_projection_from_bounds(0,
                                                                            self.GetSize().width,
                                                                            0,
                                                                            self.GetSize().height,
                                                                            0,
                                                                            1)

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

        # update cell position
        cell_centers = format_epithelium_for_gl(self.epithelium)  # type: numpy.ndarray
        cell_count = len(cell_centers)  # type: int
        if cell_count <= self._gl_reserved_cell_count:
            self.vbo.orphan()
            if cell_count < self._gl_reserved_cell_count:
                # clear the vbo so that previously drawn cells don't remain on screen
                self.vbo.clear()
            self.vbo.write(cell_centers.astype('f4').tobytes())
        else:
            # create new vao and vbo to store larger data size
            # TODO: find a way to increase the size of the vbo without creating a new vao
            # This is probably suboptimal performance wise (especially since we will be frequently)
            gl_cells = format_epithelium_for_gl(self.epithelium).astype('f4').tobytes()
            self.vbo = self.context.buffer(gl_cells, dynamic=True)
            self.vao = self.context.simple_vertex_array(self.__program, self.vbo, ['vert'])
            self._gl_reserved_cell_count = len(cell_centers)

        # update the model (zoom / pan)
        model = matrix44.multiply(self.__translate_matrix, self.__scale_matrix)  # type: numpy.ndarray
        self.__program.uniforms["model"].value = tuple(model.flatten())

        projection = matrix44.create_perspective_projection_from_bounds(0,
                                                                        self.GetSize().width,
                                                                        0,
                                                                        self.GetSize().height,
                                                                        0,
                                                                        1)
        # self.__program.uniforms["projection"].value = tuple(projection.flatten())

        self.vao.render(mode=ModernGL.POINTS)

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

        # get shader code
        vertex_shader_path = r"display_2d/shaders/SimplePoints.vert"
        with open(vertex_shader_path, "r") as vertex_shader_file:
            vertex_shader_string = str(vertex_shader_file.read())

        # geometry shader
        geometry_shader_path = r"display_2d/shaders/CircleGenerator.geom"
        with open(geometry_shader_path, "r") as geometry_shader_file:
            geometry_shader_string = str(geometry_shader_file.read())

        # fragment shader
        fragment_shader_path = r"display_2d/shaders/SimpleColor.frag"
        with open(fragment_shader_path, "r") as fragment_shader_file:
            fragment_shader_string = str(fragment_shader_file.read())

        vert = self.context.vertex_shader(vertex_shader_string)
        geom = self.context.geometry_shader(geometry_shader_string)
        frag = self.context.fragment_shader(fragment_shader_string)

        self.__program = self.context.program([vert, geom, frag])

        self.vbo = self.context.buffer(dynamic=True, reserve=self._gl_reserved_cell_count)
        self.vao = self.context.simple_vertex_array(self.__program, self.vbo, ['vert'])

        self.__gl_initialized = True

    @property
    def epithelium(self):
        return self.GetParent().epithelium
