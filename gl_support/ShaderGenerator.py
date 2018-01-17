import os

import OpenGL.GL.shaders
from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER

from gl_support.GlHelperFunctions import check_gl_error


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

    def create_program(self, vertex_shader_name: str = "",
                       fragment_shader_name: str = ""):
        """
        Generates shader programs with the shaders that are in shader_folder_path.

        :param vertex_shader_name: Name of the vertex shader (example: VertexShader.vert)
        :param fragment_shader_name: Name of the fragment shader (example: FragmentShader.frag)
        :return: If compilation was successful return the resulting shader. If there was an error return None.
        """

        # TODO: add support for all shader types

        # vertex shader
        vertex_shader_path = os.path.join(self.shader_folder_path, vertex_shader_name)
        with open(vertex_shader_path, "r") as vertex_shader_file:
            vertex_shader_string = str.encode(vertex_shader_file.read())

        # fragment shader
        fragment_shader_path = os.path.join(self.shader_folder_path, fragment_shader_name)
        with open(fragment_shader_path, "r") as fragment_shader_file:
            fragment_shader_string = str.encode(fragment_shader_file.read())

        # compile program
        program = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader_string, GL_FRAGMENT_SHADER)
        )

        # return program
        if check_gl_error():
            return None
        return program

        return True  # not error_found
