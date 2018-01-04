from OpenGL.GL import *
from OpenGL.GLU import *
import math


def draw_circle(center: tuple = (0, 0),
                radius: float = 10,
                fill: bool = False,
                color: tuple = (1, 0, 0, 1),
                segments: int = 20) -> None:

    if fill:
        draw_mode = GL_TRIANGLE_FAN
    else:
        draw_mode = GL_LINE_LOOP

    glBegin(draw_mode)

    # set color
    glColor(color)

    # center
    if fill:
        glVertex2f(center[0], center[1])

    # draw circle
    for i in range(segments + 1):
        glVertex2f(
            center[0] + (radius * math.cos(i * (2 * math.pi) / segments)),
            center[1] + (radius * math.sin(i * (2 * math.pi) / segments))
        )
    glEnd()
