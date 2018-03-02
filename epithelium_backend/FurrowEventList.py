import eye_development_gui.FieldType as FieldType
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.FurrowEvent import FurrowEvent


def run_r8_selector(field_types, epithelium, cells):
    """R8 cell selection logic
    :param field_types: Input parameters.
      'r8 selection radius' -> the minimum number of cells (approximated) between R8 cells.
    :param epithelium: epithelium where selection is taking place.
    :param cells: Cells to run selection on (should be part of passed epithelium).
    """
    r8_exclusion_radius = field_types['r8 exclusion radius'].value
    for cell in cells:
        neighbors = epithelium.neighboring_cells(cell, r8_exclusion_radius)
        assign = True
        for neighbor in neighbors:
            if neighbor.photoreceptor_type == PhotoreceptorType.R8:
                assign = False
        if assign:
            cell.photoreceptor_type = PhotoreceptorType.R8


r8_selection_event = FurrowEvent(distance_from_furrow=0,
                                 field_types={'r8 exclusion radius': FieldType.IntegerFieldType(4)},
                                 run=run_r8_selector)

# All Furrow Events ordered from first to last
furrow_event_list = [r8_selection_event]
