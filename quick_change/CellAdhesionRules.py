from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.SupportCellType import SupportCellType


def determine_cell_adhesion(first_cell: Cell, second_cell: Cell) -> float:
    """
    Determine how adhesive one cell is to another. The more adhesive a cell is to
    another the more they will stick together.
    Cell adhesion is not necessarily symmetric.
    :param first_cell: The cell that is actively adhering to a target cell
    :param second_cell: The target cell that is being adhered to
    :return: Adhesion factor representing how adhesive firstCell is to second_cell. The greater the adhesion factor the
            more the cells will stick together
    """

    # most cells use this adhesion coefficient
    standard_adhesion_coefficient = 0.32

    # Non photoreceptor cells interact normally
    if first_cell.photoreceptor_type is PhotoreceptorType.NOT_RECEPTOR:
        return standard_adhesion_coefficient
    # both cells are receptors
    elif second_cell.photoreceptor_type is not PhotoreceptorType.NOT_RECEPTOR:
        return 2 * standard_adhesion_coefficient
    # Boarder cell adhesion
    elif SupportCellType.BORDER_CELL in first_cell.support_specializations:
        # to receptor cells
        if second_cell.photoreceptor_type is not PhotoreceptorType.NOT_RECEPTOR:
            return 2 * standard_adhesion_coefficient
        # to border cells
        elif SupportCellType.BORDER_CELL in second_cell.support_specializations:
            return 1.5 * standard_adhesion_coefficient

    # catch all unspecified
    return standard_adhesion_coefficient
