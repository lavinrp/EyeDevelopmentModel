from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType


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
