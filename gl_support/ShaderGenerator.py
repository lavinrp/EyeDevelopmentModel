import OpenGL.GL.shaders
from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER


class ShaderGenerator:
    """Manages creation of OpenGL shader programs."""

    def __init__(self, shader_folder_path: str = "") -> None:
        """
        Initializes this instance of ShaderGenerator. Stores the file path to the shaders that will be used for
        shader program generation.
        :param shader_folder_path: File path to the folder that contains all the shaders that will be compiled to a
        shader program.
        """

        self.shader_folder_path = shader_folder_path

        # Compiled shader program
        self.program = None

        # store all compile errors here
        self.errors = ""  # type: str

    def create_program(self) -> bool:
        """
        Generate a shader program with the shaders that are in shader_folder_path.
        The generated program is stored in self.program.

        All shaders are expected to be in a file named after the type of the shader (vertex.sh, fragment.sh, etc...).

        :return: True if no errors are detected when compiling the shader program. False otherwise.
        """

        # TODO: add support for all shader types
        # TODO: change system to find shaders based on extension
        #   https://stackoverflow.com/a/26531467

        # vertex shader
        with open(self.shader_folder_path + r"/vertex.sh", "r") as vertex_shader_file:
            vertex_shader_string = str.encode(vertex_shader_file.read())

        # fragment shader
        with open(self.shader_folder_path + r"/fragment.sh", "r") as fragment_shader_file:
            fragment_shader_string = str.encode(fragment_shader_file.read())

        # compile program
        self.program = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader_string, GL_FRAGMENT_SHADER)
        )

        # # check for errors
        # error_found = False
        # compile_status = OpenGL.GL.glGetShaderiv(vertex_shader_string, GL_COMPILE_STATUS)
        # if compile_status != GL_TRUE:
        #     self.errors += "\n" + OpenGL.GL.glGetShaderInfoLog(vertex_shader_string)
        #     error_found = True
        # compile_status = OpenGL.GL.glGetShaderiv(fragment_shader_string, GL_COMPILE_STATUS)
        # if compile_status != GL_TRUE:
        #     self.errors += "\n" + OpenGL.GL.glGetShaderInfoLog(vertex_shader_string)
        #     error_found = True

        return True  # not error_found

        # TODO: check for linking errors
