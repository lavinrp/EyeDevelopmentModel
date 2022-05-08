from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.SupportCellType import SupportCellType


def determine_cell_color(cell: Cell) -> tuple:
    """
    Determines the color that the passed cell should be drawn with based on its properties.
    :param cell: The cell whose color will be determined.
    """
    if cell.photoreceptor_type == PhotoreceptorType.R1:
        return .98, .72, 96
    elif cell.photoreceptor_type == PhotoreceptorType.R2:
        return .85, .3, 0.9
    elif cell.photoreceptor_type == PhotoreceptorType.R3:
        return .95, .45, .9
    elif cell.photoreceptor_type == PhotoreceptorType.R4:
        return .95, .45, .9
    elif cell.photoreceptor_type == PhotoreceptorType.R5:
        return .85, .3, .9
    elif cell.photoreceptor_type == PhotoreceptorType.R6:
        return .98, .72, .96
    elif cell.photoreceptor_type == PhotoreceptorType.R7:
        return .8, .3, 1
    elif cell.photoreceptor_type == PhotoreceptorType.R8:
        return .65, .03, .65
    elif cell.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR \
            and SupportCellType.BORDER_CELL in cell.support_specializations:
        return .2, 1, .2
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
       cell.photoreceptor_type == PhotoreceptorType.R8 or \
       SupportCellType.BORDER_CELL in cell.support_specializations:
        return True
    else:
        return False
