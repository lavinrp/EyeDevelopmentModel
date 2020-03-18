from typing import Tuple

import moderngl
from pyrr import matrix44

from .EpitheliumGlTranslator import format_epithelium_for_gl, gl_bytes_per_cell
from .Simple2dGlProgram import Simple2dGlProgram
from epithelium_backend.Epithelium import Epithelium


vertex_shader_path = "display_2d/shaders/CircleGenerator.vert"
empty_geometry_shader_path = "display_2d/shaders/EmptyCircleGenerator.geom"
filled_geometry_shader_path = "display_2d/shaders/FilledCircleGenerator.geom"
fragment_shader_path = "display_2d/shaders/CircleGenerator.frag"


class EpitheliumScene:
    """The OpenGL scene displayed in an EpitheliumWidget."""

    # A class epithelium instance for all scenes to use
    _epithelium = Epithelium(0)

    # Class variables for camera settings so all scenes are synced
    _camera_x = 0
    _camera_y = 0
    _scale = 1.0

    def __init__(self, ctx):
        self._ctx = ctx

        self._camera_up_vector = [0, 1, 0]
        self._translate_matrix = matrix44.create_identity()

        self._empty_circle_gl_program = Simple2dGlProgram()
        self._empty_circle_gl_program.reserved_object_count = 1000
        self._empty_circle_gl_program.reserved_object_bytes = gl_bytes_per_cell
        self._empty_circle_gl_program.context = self._ctx
        self._empty_circle_gl_program.create_program(
            vertex_shader_path, empty_geometry_shader_path, fragment_shader_path
        )
        self._empty_circle_gl_program.init_vertex_objects('2f 3f 1f', ['vert', 'vert_color', 'vert_radius'])

        self._filled_circle_gl_program = Simple2dGlProgram()
        self._filled_circle_gl_program.reserved_object_count = 500
        self._filled_circle_gl_program.reserved_object_bytes = gl_bytes_per_cell
        self._filled_circle_gl_program.context = self._ctx
        self._filled_circle_gl_program.create_program(
            vertex_shader_path, filled_geometry_shader_path, fragment_shader_path
        )
        self._filled_circle_gl_program.init_vertex_objects('2f 3f 1f', ['vert', 'vert_color', 'vert_radius'])

    def clear(self, color: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        """
        Clear the bound framebuffer.
        :param color: A 4-tuple to clear with (R, G, B, A)
        """
        self._ctx.clear(*color)

    def draw(self):
        """Draw the epithelium scene."""
        # Update cell positions
        cell_data = format_epithelium_for_gl(self.epithelium)
        self._empty_circle_gl_program.update_vertex_objects(cell_data[0])
        self._filled_circle_gl_program.update_vertex_objects(cell_data[1])

        # Update the model view projection matrix
        model = matrix44.multiply(self._translate_matrix, self._scale_matrix)
        model_view_matrix = matrix44.multiply(self._view_matrix, model)
        model_view_projection_matrix = matrix44.multiply(self._projection_matrix, model_view_matrix)

        model_view_projection_tuple = tuple(model_view_projection_matrix.flatten())
        self._empty_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple
        self._filled_circle_gl_program.program["model_view_projection"].value = model_view_projection_tuple

        # Render to screen
        self._empty_circle_gl_program.vao.render(mode=moderngl.POINTS)
        self._filled_circle_gl_program.vao.render(mode=moderngl.POINTS)

    def resize(self, ctx: moderngl.Context):
        """
        Adjusts the camera view based on an adjusted context.
        :param ctx: The adjusted context
        """
        self._ctx = ctx

    @staticmethod
    def pan(x: int, y: int):
        """
        Pans the camera around the scene.
        :param x: X coordinate to pan to
        :param y: Y coordinate to pan to
        :return:
        """
        EpitheliumScene._camera_x = x
        EpitheliumScene._camera_y = y

    @staticmethod
    def zoom(rotation: int):
        """
        Zooms the camera in or out of the scene.
        :param rotation: The rotation delta, used to determine direction of zoom
        """
        if rotation < 0:
            EpitheliumScene._scale *= 0.9
        elif rotation > 0:
            EpitheliumScene._scale *= 1.1

    @property
    def epithelium(self) -> Epithelium:
        """The class epithelium instance."""
        return EpitheliumScene._epithelium

    @epithelium.setter
    def epithelium(self, epithelium):
        EpitheliumScene._epithelium = epithelium

    @property
    def _projection_matrix(self) -> matrix44:
        return matrix44.create_orthogonal_projection_matrix(
            0, self._ctx.viewport[2], 0, self._ctx.viewport[3], 1, 2
        )

    @property
    def _view_matrix(self) -> matrix44:
        return matrix44.create_look_at(
            [EpitheliumScene._camera_x, EpitheliumScene._camera_y, 0],
            [EpitheliumScene._camera_x, EpitheliumScene._camera_y, -1],
            self._camera_up_vector
        )

    @property
    def _scale_matrix(self) -> matrix44:
        return matrix44.create_from_scale((EpitheliumScene._scale, EpitheliumScene._scale, 1))
