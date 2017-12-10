import OpenGL.GL.shaders
from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER


class ShaderGenerator:
    """Manages creation of OpenGL shader programs."""

    def __init__(self, shader_folder_path=""):
        """
        Initializes this instance of ShaderGenerator. Stores the file path to the shaders that will be used for
        shader program generation.
        :param shader_folder_path: File path to the folder that contains all the shaders that will be compiled to a
        shader program.
        """

        self.shader_folder_path = shader_folder_path

        # Compiled shader program
        self.program = None

    def create_program(self):
        """Generate a shader program with the shaders that are in shader_folder_path."""

        # TODO: add support for all shader types

        with open(self.shader_folder_path + r"/vertex.sh", "r") as vertex_shader_file:
            vertex_shader_string = vertex_shader_file.read()

        with open(self.shader_folder_path + r"/fragment.sh", "r") as fragment_shader_file:
            fragment_shader_string = fragment_shader_file.read()

        return OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader_string, GL_FRAGMENT_SHADER)
        )


