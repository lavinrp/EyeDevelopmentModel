from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
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


def determine_cell_color(cell: Cell) -> tuple:
    """
    Determines the color that the passed cell should be drawn with based on its properties.
    :param cell: The cell whose color will be determined.
    """

    if cell.photoreceptor_type == PhotoreceptorType.R1:
        return 0, .5, .4  # turquoise
    if cell.photoreceptor_type == PhotoreceptorType.R2:
        return .5, 0, .25  # Burgundy
    if cell.photoreceptor_type == PhotoreceptorType.R3:
        return .5, .5, 0   # olive
    if cell.photoreceptor_type == PhotoreceptorType.R4:
        return .25, .25, 0   # forest green
    if cell.photoreceptor_type == PhotoreceptorType.R5:
        return .25, 0, .25   # Dark Purple
    if cell.photoreceptor_type == PhotoreceptorType.R6:
        return .5, .25, .5  # Lavender
    if cell.photoreceptor_type == PhotoreceptorType.R7:
        return .5, 70, .5  # Pistachio
    if cell.photoreceptor_type == PhotoreceptorType.R8:
        return 1, 0, 0
    else:
        return 0, 0, 1


def determine_cell_fill(cell: Cell) -> bool:
    """
    Determines if the passed cell should be drawn as hollow or filled
    :param cell: The cell to have fill status checked
    :return: True if the cell should be filled, false otherwise.
    """
    if cell.photoreceptor_type == PhotoreceptorType.R1 or \
       cell.photoreceptor_type == PhotoreceptorType.R2 or \
       cell.photoreceptor_type == PhotoreceptorType.R3 or \
       cell.photoreceptor_type == PhotoreceptorType.R4 or \
       cell.photoreceptor_type == PhotoreceptorType.R5 or \
       cell.photoreceptor_type == PhotoreceptorType.R6 or \
       cell.photoreceptor_type == PhotoreceptorType.R7 or \
       cell.photoreceptor_type == PhotoreceptorType.R8:
        return True
    else:
        return False
