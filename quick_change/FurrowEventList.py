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
            cell.dividable = False


r8_selection_event = FurrowEvent(distance_from_furrow=0,
                                 field_types={'r8 exclusion radius': FieldType.IntegerFieldType(4)},
                                 run=run_r8_selector)


def run_r2_r5_selector(field_types, epithelium, cells):
    """R2 and R5 cell selection logic
    :param field_types: Input parameters.
    :param epithelium: epithelium where selection is taking place.
    :param cells: Cells to run selection on (should be part of passed epithelium).
    """

    for cell in cells:
        if cell.photoreceptor_type is PhotoreceptorType.R8:
            neighbors = epithelium.neighboring_cells(cell, 2)
            neighbors.sort(key=cell.distance_to_other)
            chosen_count = 0
            for neighbor in neighbors:
                if chosen_count is field_types["r2, r5 selection count"].value:
                    break
                if neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 0:
                    neighbor.photoreceptor_type = PhotoreceptorType.R2
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R5
                    neighbor.dividable = False
                    chosen_count += 1


r2_r5_selection_event = FurrowEvent(distance_from_furrow=100,
                                    field_types={"r2, r5 selection count": FieldType.IntegerFieldType(2)},
                                    run=run_r2_r5_selector)


def run_r3_r4_selector(field_types, epithelium, cells):
    """R3 and R4 cell selection logic
    :param field_types: Input parameters.
    :param epithelium: epithelium where selection is taking place.
    :param cells: Cells to run selection on (should be part of passed epithelium).
    """

    for cell in cells:
        if cell.photoreceptor_type is PhotoreceptorType.R8:
            neighbors = epithelium.neighboring_cells(cell, 2)
            neighbors.sort(key=cell.distance_to_other)
            chosen_count = 0
            for neighbor in neighbors:
                if chosen_count is field_types["r3, r4 selection count"].value:
                    break
                if neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 0:
                    neighbor.photoreceptor_type = PhotoreceptorType.R3
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R4
                    neighbor.dividable = False
                    chosen_count += 1


r3_r4_selection_event = FurrowEvent(distance_from_furrow=150,
                                    field_types={"r3, r4 selection count": FieldType.IntegerFieldType(2)},
                                    run=run_r3_r4_selector)


def run_r1_r6_selector(field_types, epithelium, cells):
    """R1 and R6 cell selection logic
    :param field_types: Input parameters.
    :param epithelium: epithelium where selection is taking place.
    :param cells: Cells to run selection on (should be part of passed epithelium).
    """

    for cell in cells:
        if cell.photoreceptor_type is PhotoreceptorType.R8:
            neighbors = epithelium.neighboring_cells(cell, 4)
            neighbors.sort(key=cell.distance_to_other)
            chosen_count = 0
            for neighbor in neighbors:
                if chosen_count is field_types["r1, r6 selection count"].value:
                    break
                if neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 0:
                    neighbor.photoreceptor_type = PhotoreceptorType.R1
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R6
                    neighbor.dividable = False
                    chosen_count += 1


r1_r6_selection_event = FurrowEvent(distance_from_furrow=200,
                                    field_types={"r1, r6 selection count": FieldType.IntegerFieldType(2)},
                                    run=run_r1_r6_selector)

# All Furrow Events ordered from first to last
furrow_event_list = [r8_selection_event,
                     r2_r5_selection_event,
                     r3_r4_selection_event,
                     r1_r6_selection_event]
