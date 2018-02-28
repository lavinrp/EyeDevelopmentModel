from OpenGL.GL import *
import math


def draw_circle(center: tuple = (0, 0),
                radius: float = 10,
                fill: bool = False,
                color: tuple = (1, 0, 0, 1),
                segments: int = 20) -> None:
    """
    Draws a circle to an using OpenGL context mode
    :param center: The center position of the circle
    :param radius: The radius of the circle
    :param fill:  If true the circle will be filled with a solid color. If false the circle will simply be a perimeter.
    :param color: The RGBA color of the circle
    :param segments: The number of line segments with which to make the circle.
        (The 'circle' is simply a polygon with many sides)
    """
    if fill:
        draw_mode = GL_TRIANGLE_FAN
    else:
        draw_mode = GL_LINE_LOOP

    glBegin(draw_mode)

    # set color
    glColor(color)

    # center
    if fill:
        glVertex3f(center[0], center[1], 0)

    # draw circle
    for i in range(segments + 1):
        glVertex3f(
            center[0] + (radius * math.cos(i * (2 * math.pi) / segments)),
            center[1] + (radius * math.sin(i * (2 * math.pi) / segments)),
            0
        )
    glEnd()
