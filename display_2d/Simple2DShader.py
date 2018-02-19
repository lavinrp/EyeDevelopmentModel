import ModernGL
import numpy


class Simple2DShader(object):
    """Convenience class to gather all data and functions for easy drawing of 2d objects"""

    def __init__(self, context: ModernGL.Context=None):
        """Initialize this instance of Simple2DShader"""
        self.context = context  # type: ModernGL.Context
        self.vao_content = []  # type: list
        self.vao = None  # type: ModernGL.VertexArray
        self.vbo = None  # type: ModernGL.Buffer
        self.program = None  # type: ModernGL.Program

        # the number of instances to reserve memory for
        self.reserved_object_count = 0  # type: int

        # the number of bytes per reserved object
        self.reserved_object_bytes = 0  # type: int

    def create_program(self,
                       vertex_shader_path: str = "",
                       geometry_shader_path: str = "",
                       fragment_shader_path: str = "") -> None:
        """
        Creates the shader program with passed vertex, geometry, and fragment shaders.
        :param vertex_shader_path: Path to the vertex shader file.
        :param geometry_shader_path: Path to the geometry shader file.
        :param fragment_shader_path: Path to the fragment shader file.
        """
        # read shaders
        with open(vertex_shader_path, "r") as vertex_shader_file:
            vertex_shader_string = str(vertex_shader_file.read())
        with open(geometry_shader_path, "r") as geometry_shader_file:
            geometry_shader_string = str(geometry_shader_file.read())
        with open(fragment_shader_path, "r") as fragment_shader_file:
            fragment_shader_string = str(fragment_shader_file.read())

        # create shader program
        vert = self.context.vertex_shader(vertex_shader_string)
        geom = self.context.geometry_shader(geometry_shader_string)
        frag = self.context.fragment_shader(fragment_shader_string)
        self.program = self.context.program([vert, geom, frag])

    def init_vertex_objects(self, vao_format: str, vao_inputs: list):
        """
        Initializes the vbo, vao and vao_content for this Simple2DShader
        :param vao_format: The per-input byte format of the shader inputs.
        :param vao_inputs: The names of all shader inputs.
        """
        # vao and vbo init
        self.vbo = \
            self.context.buffer(dynamic=True, reserve=self.reserved_object_count * self.reserved_object_bytes)
        self.vao_content = [(self.vbo, vao_format, vao_inputs)]
        self.vao = self.context.vertex_array(self.program, self.vao_content)

    def update_vertex_objects(self, input_data: numpy.ndarray):
        """
        updates the vao, vbo and vao_content with new data
        :param input_data: The new data
        """
        input_data_count = len(input_data)  # type: int
        gl_data = input_data.astype('f4').tobytes()  # type: bytearray

        if input_data_count <= self.reserved_object_count:
            self.vbo.orphan()
            if input_data_count < self.reserved_object_count:
                # clear the vbo so that previously drawn objects don't remain on screen
                self.vbo.clear()
            self.vbo.write(gl_data)

        else:
            # create new vao and vbo to store larger data size
            # TODO: find a way to increase the size of the vbo without creating a new vao
            # This is probably suboptimal performance wise (especially since we will be frequently)
            self.vbo = self.context.buffer(gl_data, dynamic=True)
            self.vao_content[0] = (self.vbo, self.vao_content[0][1], self.vao_content[0][2])
            self.vao = self.context.vertex_array(self.program, self.vao_content)

            self.reserved_object_count = input_data_count

