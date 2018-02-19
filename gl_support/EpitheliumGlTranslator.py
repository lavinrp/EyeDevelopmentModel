from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
import numpy
import math


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
    if cell.photoreceptor_type == PhotoreceptorType.R8:
        return True
    else:
        return False


class EpitheliumGlTranslator:
    """Translates the epithelium into data that can be displayed via OpenGL"""

    def __init__(self, epithelium: Epithelium = None) -> None:
        """
        Initializes this instance of EpitheliumGlTranslator.
        :param epithelium: The epithelium to be translated. Defaults to None.
        """
        self.epithelium = epithelium  # type: Epithelium

    def get_line_loop_points(self, segments):
        cell_list_points = [self.epithelium.cell_quantity * segments]
        for cell in self.epithelium.cells:
            for i in range(segments + 1):
                cell_list_points[i].append(
                    cell.position[0] + (cell.radius * math.cos(i * (2 * math.pi) / segments)),
                    cell.position[1] + (cell.radius * math.sin(i * (2 * math.pi) / segments)),
                    0)
        return cell_list_points
