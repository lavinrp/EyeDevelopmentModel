import os

import wx
from wx import glcanvas
import moderngl
from pyrr import matrix44
from pyrr import vector4
import numpy

from display_2d.EpitheliumGlTranslator import format_epithelium_for_gl
from display_2d.EpitheliumGlTranslator import gl_bytes_per_cell
from display_2d.Simple2dGlProgram import Simple2dGlProgram
from display_2d.GlHelpers import world_coord_from_window_coord
from legacy_display_2d.LegacyDisplayCanvas import LegacyDisplayCanvas


class ModernDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        if not os.getenv("eye_develop_model_no_ogl_core"):
            attribute_list = [glcanvas.WX_GL_CORE_PROFILE, glcanvas.WX_GL_DOUBLEBUFFER, 0]
        else:
            attribute_list = None

        glcanvas.GLCanvas.__init__(self,
                                   parent,
                                   size=(parent.GetSize()),
                                   name='epithelium_display_canvas',
                                   attribList=attribute_list)
        # GL
        self.wx_context = None  # type:  glcanvas.GLContext
        self.context = None  # type: moderngl.Context
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 1.0  # type: float
        self.__camera_up_vector = [0, 1, 0]

        self.__scale_matrix = matrix44.create_from_scale((self.__scale,
                                                          self.__scale,
                                                          self.__scale))  # type: numpy.ndarray
        self.__translate_matrix = matrix44.create_identity()
        self.__projection_matrix = matrix44.create_orthogonal_projection_matrix(0,
                                                                                self.GetSize().width,
                                                                                0,
                                                                                self.GetSize().height,
                                                                                1,
                                                                                2)
        self.__view_matrix = matrix44.create_look_at([self.__camera_x, self.__camera_y, 0],
                                                     [self.__camera_x, self.__camera_y, -1],
                                                     self.__camera_up_vector)

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
        self._pan_speed = 1  # type: float
        self.__last_mouse_position = [0, 0]  # type: list
        self.camera_listeners = []  # type: list

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
        if self.wx_context:
            self.SetCurrent(self.wx_context)
        size = self.GetParent().GetSize()
        self.SetSize(size)
        if self.context:
            self.context.viewport = (0, 0, size.width, size.height)

        self.__projection_matrix = matrix44.create_orthogonal_projection_matrix(0,
                                                                                self.GetSize().width,
                                                                                0,
                                                                                self.GetSize().height,
                                                                                1,
                                                                                2)
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
                # get world position of mouse
                last_mouse_world_position = world_coord_from_window_coord(self.__last_mouse_position,
                                                                          list(self.GetSize()),
                                                                          self.model_view_matrix)
                mouse_world_position = world_coord_from_window_coord(current_mouse_position,
                                                                     list(self.GetSize()),
                                                                     self.model_view_matrix)

                # pan camera by how far the mouse moved in world coordinates
                world_delta_x = last_mouse_world_position[0] - mouse_world_position[0]
                world_delta_y = -(last_mouse_world_position[1] - mouse_world_position[1])
                self.pan_camera(world_delta_x, world_delta_y)

        # scroll wheel
        wheel_rotation = event.GetWheelRotation()
        if wheel_rotation > 0:
            self.set_scale(1.1)
        elif wheel_rotation < 0:
            self.set_scale(0.9)

        # update mouse position
        self.__last_mouse_position = current_mouse_position

    def pan_camera(self, delta_x: float, delta_y: float, active_canvas: bool = True) -> None:
        """Pan the camera by the specified deltas
        :param delta_x: change in the x of the camera
        :param delta_y: change in the y of the camera
        :param active_canvas: An active canvas repaints and signals all of its camera_listeners to pan.
        """

        self.__camera_x += delta_x * self._pan_speed
        self.__camera_y -= delta_y * self._pan_speed

        self.__view_matrix = matrix44.create_look_at([self.__camera_x, self.__camera_y, 0],
                                                     [self.__camera_x, self.__camera_y, -1],
                                                     self.__camera_up_vector)

        if active_canvas:
            for listener in self.camera_listeners:
                listener.pan_camera(delta_x, delta_y, False)
            self.on_paint()

    def set_scale(self, relative_scale: float, active_canvas: bool = True) -> None:
        """
        Scales the displayed epithelium and scales the speed of panning the epithelium.
        :param active_canvas: An active canvas repaints and signals all of its camera_listeners to set their scale.
        :param relative_scale: The scale of the new display represented as a fraction of the previous scale
        Example: 1.1 with an original scale of 2.0 will produce a new scale of 2.2.
        :return:
        """
        self.__scale *= relative_scale
        self.__scale_matrix = matrix44.create_from_scale((self.__scale,
                                                          self.__scale,
                                                          1))  # type: numpy.ndarray
        if active_canvas:
            for listener in self.camera_listeners:
                listener.set_scale(relative_scale, False)
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

        # update the model view projection matrix
        model_view_projection_tuple = tuple(self.model_view_projection_matrix.flatten())
        self.empty_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple
        self.filled_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple

        # render to screen
        self.empty_circle_gl_program.vao.render(mode=moderngl.POINTS)
        self.filled_circle_gl_program.vao.render(mode=moderngl.POINTS)
        self.SwapBuffers()

    def _init_gl(self) -> None:
        """
        Initializes all internal OpenGL elements (Shader Program, gl context, etc...).
        Sets __gl_initialized to true.
        """

        # context setup
        self.wx_context = glcanvas.GLContext(self)
        self.SetCurrent(self.wx_context)
        self.context = moderngl.create_context()

        # empty circle program setup
        self.empty_circle_gl_program.context = self.context
        vertex_shader_path = r"display_2d/shaders/CircleGenerator.vert"
        geometry_shader_path = r"display_2d/shaders/EmptyCircleGenerator.geom"
        fragment_shader_path = r"display_2d/shaders/CircleGenerator.frag"
        self.empty_circle_gl_program.create_program(vertex_shader_path, geometry_shader_path, fragment_shader_path)
        self.empty_circle_gl_program.init_vertex_objects('2f 3f 1f', ['vert', 'vert_color', 'vert_radius'])

        # filled circle program setup
        self.filled_circle_gl_program.context = self.context
        vertex_shader_path = r"display_2d/shaders/CircleGenerator.vert"
        geometry_shader_path = r"display_2d/shaders/FilledCircleGenerator.geom"
        fragment_shader_path = r"display_2d/shaders/CircleGenerator.frag"
        self.filled_circle_gl_program.create_program(vertex_shader_path, geometry_shader_path, fragment_shader_path)
        self.filled_circle_gl_program.init_vertex_objects('2f 3f 1f', ['vert', 'vert_color', 'vert_radius'])

        self.__gl_initialized = True

    @property
    def epithelium(self):
        return self.GetParent().epithelium

    @property
    def model_view_projection_matrix(self) -> numpy.ndarray:
        """Returns the model view projection matrix of the current scene."""
        # update the model (zoom / pan)
        return matrix44.multiply(self.__projection_matrix, self.model_view_matrix)

    @property
    def model_view_matrix(self) -> numpy.ndarray:
        """
        Returns the model view matrix of the current scene.
        """
        model = matrix44.multiply(self.__translate_matrix, self.__scale_matrix)  # type: numpy.ndarray
        return matrix44.multiply(self.__view_matrix, model)


class EpitheliumDisplayCanvas(LegacyDisplayCanvas if os.getenv("eye_develop_model_legacy_display")
                              else ModernDisplayCanvas):
    pass
