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

        # Three vertices, with an x,y,z & w for each.
        vertexPositions = [
            0.0, 1.0,
            1.0, 0.0,
            0.0, -1.0,
            -1.0, 0.0,
        ]

        vao = OpenGL.GL.glGenVertexArrays(1)
        OpenGL.GL.glBindVertexArray(vao)
        vbo = OpenGL.GL.glGenBuffers(1)
        OpenGL.GL.glBindBuffer(OpenGL.GL.GL_ARRAY_BUFFER, vbo)
        array_type = (OpenGL.GL.GLfloat * len(vertexPositions))
        OpenGL.GL.glBufferData(OpenGL.GL.GL_ARRAY_BUFFER,
                               len(vertexPositions) * 4,
                               array_type(*vertexPositions),
                               OpenGL.GL.GL_STATIC_DRAW)
        OpenGL.GL.glVertexAttribPointer(0, 2, OpenGL.GL.GL_FLOAT, OpenGL.GL.GL_FALSE, 0, 0)
        OpenGL.GL.glEnableVertexAttribArray(0)

        strVertexShader = """
        #version 120
        in vec4 position;
        void main()
        {
           gl_Position = position;
        }
        """
        strFragmentShader = """
        #version 120
        out vec4 outputColor;
        void main()
        {
           outputColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
        }
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

        # # compile program
        # program = OpenGL.GL.shaders.compileProgram(
        #     OpenGL.GL.shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER),
        #     OpenGL.GL.shaders.compileShader(fragment_shader_string, GL_FRAGMENT_SHADER)
        # )
        vertex_shader = OpenGL.GL.shaders.compileShader(strVertexShader, GL_VERTEX_SHADER)
        vert_compiled = OpenGL.GL.glGetShaderiv(vertex_shader, OpenGL.GL.GL_COMPILE_STATUS)
        if not vert_compiled:
            print("vertex compile error")
            raise RuntimeError(OpenGL.GL.glGetShaderInfoLog(vertex_shader))

        fragment_shader = OpenGL.GL.shaders.compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
        frag_compiled = OpenGL.GL.glGetShaderiv(fragment_shader, OpenGL.GL.GL_COMPILE_STATUS)
        if not frag_compiled:
            print("fragment compile error")
            raise RuntimeError(OpenGL.GL.glGetShaderInfoLog(fragment_shader))

        program = OpenGL.GL.glCreateProgram()
        OpenGL.GL.glAttachShader(program, vertex_shader)
        OpenGL.GL.glAttachShader(program, fragment_shader)

        OpenGL.GL.glBindAttribLocation(program, 0, "position")

        OpenGL.GL.glLinkProgram(program)
        # program_linked = OpenGL.GL.glGetShaderiv(program, OpenGL.GL.GL_LINK_STATUS)
        program_linked_message = OpenGL.GL.glGetProgramInfoLog(program)
        if program_linked_message:
            print("program link message: " + program_linked_message)



        # return program
        if check_gl_error():
            return None
        return program

        return True  # not error_found
