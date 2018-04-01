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
from legacy_display_2d.LegacyDisplayCanvas import LegacyDisplayCanvas


class ModernDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent: wx.Panel):
        glcanvas.GLCanvas.__init__(self, parent, size=(parent.GetSize()), name='epithelium_display_canvas')
        # GL
        self.wx_context = None  # type:  glcanvas.GLContext
        self.context = None  # type: moderngl.Context
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 1.0  # type: float
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
        self._pan_speed = 0.01  # type: float
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
            print(self.world_coord_from_window_coord(current_mouse_position))

            self.__panning = True

        # left mouse button up
        if event.ButtonUp(wx.MOUSE_BTN_LEFT):
            self.__panning = False

        # mouse drag
        if event.Dragging():

            # panning
            if self.__panning:
                # get world position of mouse
                last_mouse_world_position = self.world_coord_from_window_coord(self.__last_mouse_position)
                mouse_world_position = self.world_coord_from_window_coord(current_mouse_position)

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

        self.__camera_x -= delta_x * self._pan_speed
        self.__camera_y -= delta_y * self._pan_speed

        self.__translate_matrix = matrix44.create_from_translation((self.__camera_x,
                                                                    self.__camera_y,
                                                                    0))  # type: numpy.ndarray
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

    # def world_coord_from_window_coord(self, window_coord: list):
    #     """
    #     Calculates the in-world (OpenGL coordinate system) coordinate the corresponds to the passed window coordinate.
    #     from http://webglfactory.blogspot.com/2011/05/how-to-convert-world-to-screen.html.
    #     :param window_coord: The window coordinate to be converted to the openGL coordinate space.
    #     :return: The in-world (OpenGL) coordinate that corresponds to the passed window coordinate (z will always be 0).
    #     """
    #
    #     canvas_width = self.GetSize().width
    #     canvas_height = self.GetSize().height
    #
    #     x = 2.0 * window_coord[0] / canvas_width - 1
    #     y = 2.0 * window_coord[1] / canvas_height + 1
    #
    #     # TODO: clean up the matrix stuff so that there no duplicated code between this and draw
    #     projection = matrix44.create_orthogonal_projection_matrix(0,
    #                                                               canvas_width,
    #                                                               0,
    #                                                               canvas_height,
    #                                                               1,
    #                                                               1.1)
    #     model = matrix44.multiply(self.__translate_matrix, self.__scale_matrix)  # type: numpy.ndarray
    #     model = matrix44.multiply(projection, model)
    #     inverse_model_projection_matrix = matrix44.inverse(model)
    #     position = vector4.create(x, y, 0, 0)
    #     position = matrix44.multiply(inverse_model_projection_matrix, position)
    #
    #     return [position[0], position[1]]

    def world_coord_from_window_coord(self, window_coord) -> list:
        """
        from https://stackoverflow.com/a/7702895
        :param window_coord:
        :return:
        """

        canvas_width = self.GetSize().width
        canvas_height = self.GetSize().height

        x = 2.0 * window_coord[0] / canvas_width - 1
        y = 1.0 - (2.0 * window_coord[1] / canvas_height)

        scale_matrix = matrix44.create_from_scale((self.__scale,
                                                   self.__scale,
                                                   1))  # type: numpy.ndarray

        translate_matrix = matrix44.create_from_translation((self.__camera_x,
                                                             self.__camera_y,
                                                             0))  # type: numpy.ndarray
        projection_matrix = \
            matrix44.create_orthogonal_projection_matrix(0,
                                                         self.GetSize().width,
                                                         0,
                                                         self.GetSize().height,
                                                         1,
                                                         1.1)

        # update the model (zoom / pan)
        model = matrix44.multiply(translate_matrix, scale_matrix)  # type: numpy.ndarray
        model = matrix44.multiply(projection_matrix, model)

        inverse_model_projection_matrix = matrix44.inverse(model)
        position = vector4.create(x, y, 0, 1)
        position = matrix44.multiply(inverse_model_projection_matrix, position)

        return [position[0], -position[1]]

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

        projection = matrix44.create_orthogonal_projection_matrix(0,
                                                                  self.GetSize().width,
                                                                  0,
                                                                  self.GetSize().height,
                                                                  1,
                                                                  1.1)

        # update the model (zoom / pan)
        model = matrix44.multiply(self.__translate_matrix, self.__scale_matrix)  # type: numpy.ndarray
        # No view so model_view == model
        model_view_projection = matrix44.multiply(projection, model)

        model_view_projection_tuple = tuple(model_view_projection.flatten())
        self.empty_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple
        self.filled_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple

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


class EpitheliumDisplayCanvas(LegacyDisplayCanvas if os.getenv("eye_develop_model_legacy_display")
                              else ModernDisplayCanvas):
    pass
