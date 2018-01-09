from OpenGL.GL import glGetError
from OpenGL.GL import GL_NO_ERROR
from OpenGL.GLU import gluErrorString


def check_gl_error():
    """Checks for an OpenGL error.
    Prints the last found OpenGL error.

    :returns: True if an error is found. Returns false otherwise."""
    if glGetError() != GL_NO_ERROR:
        print("OpenGL error: " + gluErrorString())
        return True
    return False

