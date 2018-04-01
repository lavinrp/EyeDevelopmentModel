from epithelium_backend.Epithelium import Epithelium
from quick_change.CellDisplayRules import determine_cell_color
from quick_change.CellDisplayRules import determine_cell_fill
import numpy


#              inputs * bytes per input
gl_bytes_per_cell = 6 * 4
"""The size of each cell when formatted for OpenGL
    6 float4s
    x position
    y position
    color: red value
    color: green value
    color: blue value
    radius
"""


def format_epithelium_for_gl(epithelium: Epithelium) -> list:
    """Returns a numpy array containing the center position of each cell
    :param epithelium: The epithelium to format for OpenGL
    """
    # gather the data for each cell
    empty_circle_buffer_data = []
    filled_circle_buffer_data = []
    for cell in epithelium.cells:
        if determine_cell_fill(cell):
            selected_buffer = filled_circle_buffer_data
        else:
            selected_buffer = empty_circle_buffer_data

        # gather position data
        selected_buffer.append(cell.position_x)
        selected_buffer.append(cell.position_y)

        # gather color data
        color_data = determine_cell_color(cell)
        selected_buffer.append(color_data[0])
        selected_buffer.append(color_data[1])
        selected_buffer.append(color_data[2])

        # gather radius
        selected_buffer.append(cell.radius)

    # convert to numpy array and return
    return [numpy.array(empty_circle_buffer_data, dtype=numpy.float16),
            numpy.array(filled_circle_buffer_data, dtype=numpy.float16)]
