from epithelium_backend.Epithelium import Epithelium
import numpy
import math


def format_epithelium_for_gl(epithelium: Epithelium) -> numpy.ndarray:
    """Returns a numpy array containing the center position of each cell
    :param epithelium: The epithelium to format for OpenGL
    """
    # gather the positions of each cell
    positions_list = []
    for cell in epithelium.cells:
        # The list will have the format [x1, y1, z1, x2, y2, z2...] but no z for now
        positions_list.append(cell.position_x)
        positions_list.append(cell.position_y)
    # convert to numpy array and return
    return numpy.array(positions_list, dtype=numpy.float16)


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
