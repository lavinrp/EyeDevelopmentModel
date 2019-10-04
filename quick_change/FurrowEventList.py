import eye_development_gui.FieldType as FieldType
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.FurrowEvent import FurrowEvent
from epithelium_backend.SupportCellType import SupportCellType
from quick_change.CellEvents import TryCellDeath

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
            cell.target_radius = field_types['r8 target radius'].value
            cell.dividable = False


r8_selection_event = FurrowEvent(name="R8 Selection",
                                 distance_from_furrow=0,
                                 field_types={'r8 exclusion radius': FieldType.IntegerFieldType(4),
                                              'r8 target radius': FieldType.IntegerFieldType(20)},
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
                    neighbor.target_radius = field_types["r2, r5 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R5
                    neighbor.target_radius = field_types["r2, r5 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1


r2_r5_selection_event = FurrowEvent(name="R2, R5 Selection",
                                    distance_from_furrow=100,
                                    field_types={"r2, r5 selection count": FieldType.IntegerFieldType(2),
                                                 "r2, r5 target radius": FieldType.IntegerFieldType(20)},
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
                    neighbor.target_radius = field_types["r3, r4 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R4
                    neighbor.target_radius = field_types["r3, r4 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1


r3_r4_selection_event = FurrowEvent(name="R3, R4 Selection",
                                    distance_from_furrow=150,
                                    field_types={"r3, r4 selection count": FieldType.IntegerFieldType(2),
                                                 "r3, r4 target radius": FieldType.IntegerFieldType(25)},
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
                    neighbor.target_radius = field_types["r1, r6 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1
                elif neighbor.photoreceptor_type == PhotoreceptorType.NOT_RECEPTOR and chosen_count % 2 == 1:
                    neighbor.photoreceptor_type = PhotoreceptorType.R6
                    neighbor.target_radius = field_types["r1, r6 target radius"].value
                    neighbor.dividable = False
                    chosen_count += 1


r1_r6_selection_event = FurrowEvent(name="R1, R6 Selection",
                                    distance_from_furrow=200,
                                    field_types={"r1, r6 selection count": FieldType.IntegerFieldType(2),
                                                 "r1, r6 target radius": FieldType.IntegerFieldType(25)},
                                    run=run_r1_r6_selector)


def run_border_cell_selection(field_types, epithelium, cells):
    """
    Select the cells that border the photoreceptor cells.
    :param field_types: Input parameters:
    'border radius (cells)' -> The radius (in cells) around the photoreceptor cells to specialize as border cells.
    :param epithelium: Epithelium where selection is taking place
    :param cells: Cells to run selection on (should be part of passed epithelium)
    :return:
    """
    for cell in cells:
        if cell.photoreceptor_type is PhotoreceptorType.NOT_RECEPTOR:
            distance = field_types["border radius (cells)"].value
            neighbors = epithelium.neighboring_cells(cell, distance)
            if distance == 1:
                for neighbor in neighbors:
                    if cell.touches(neighbor):
                        if neighbor.photoreceptor_type is not PhotoreceptorType.NOT_RECEPTOR:
                            # make support
                            cell.support_specializations.add(SupportCellType.BORDER_CELL)
                            cell.dividable = False
            else:
                for neighbor in neighbors:
                    if neighbor.photoreceptor_type is not PhotoreceptorType.NOT_RECEPTOR:
                        # make support
                        cell.support_specializations.add(SupportCellType.BORDER_CELL)
                        cell.dividable = False


border_cell_selection_event = FurrowEvent(name="Border Cell Selection",
                                          distance_from_furrow=250,
                                          field_types={"border radius (cells)": FieldType.IntegerFieldType(1)},
                                          run=run_border_cell_selection)


def run_cell_death(field_types, epithelium, cells):
    """
    Kill all unspecialized cells
    :param field_types: Input parameters
    :param epithelium: Epithelium where selection is taking place
    :param cells: Cells to run selection on (should be part of passed epithelium)
    :return:
    """
    for cell in cells:
        if SupportCellType.BORDER_CELL not in cell.support_specializations \
                and cell.photoreceptor_type is PhotoreceptorType.NOT_RECEPTOR:

            # only add cell event if it hasn't already been added
            # we must do this instead of letting set take care of it b/c each TryCellDeath is a different
            # instance of the class
            add_event = True
            for event in cell.cell_events:
                if isinstance(event, TryCellDeath):
                    add_event = False
            if add_event:
                cell.cell_events.add(TryCellDeath(epithelium=epithelium,
                                                  death_chance=float(field_types["death chance (0-100)"].value) / 100.0))


cell_death_event = FurrowEvent(name="Cell Death",
                               distance_from_furrow=400,
                               field_types={"death chance (0-100)": FieldType.IntegerFieldType(1)},
                               run=run_cell_death)


# All Furrow Events ordered from first to last
furrow_event_list = [r8_selection_event,
                     r2_r5_selection_event,
                     r3_r4_selection_event,
                     r1_r6_selection_event,
                     border_cell_selection_event,
                     cell_death_event]
