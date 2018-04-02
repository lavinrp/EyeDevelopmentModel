from pyrr import matrix44
from pyrr import vector4
import numpy


def world_coord_from_window_coord(window_coord: list,
                                  window_dimensions: list,
                                  model_view_matrix: numpy.ndarray) -> list:
    """
    Calculates the in-world (OpenGL coordinate system) coordinate the corresponds to the passed window coordinate.
    from https://stackoverflow.com/a/7702895
    :param window_coord: The window coordinate to be converted to the openGL coordinate space.
    :param window_dimensions: width(index 0) and height(index 1) of the window.
    :param model_view_matrix: The model view matrix being used to draw the world.
    :return: The in-world (OpenGL) 2D coordinate that corresponds to the passed window coordinate (X and Y only).
    """

    # calculate relative screen position in
    x = 2.0 * window_coord[0] / window_dimensions[0] - 1
    y = 1.0 - (2.0 * window_coord[1] / window_dimensions[1])

    # convert screen position to world space
    inverse_model_view_matrix = matrix44.inverse(model_view_matrix)
    position = vector4.create(x, y, 0, 1)
    position = matrix44.multiply(inverse_model_view_matrix, position)
    return [position[0], position[1]]
