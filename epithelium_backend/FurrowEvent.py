from epithelium_backend.PhotoreceptorType import PhotoreceptorType

class FieldType(object):
    def __init__(self, value):
        self.value = value

    def validate(self, new_val):
        """
        If new_val is a valid value for the field type,
        set it as the current value and return True. Otherwise,
        leave the value unchanged and return False.
        """
        self.value = new_val
        return True

class Integer(FieldType):
    def __init__(self, value):
        super(Integer, self).__init__(value)

    def validate(self, new_val):
        try:
            i = int(new_val)
            self.value = i
            return True
        except:
            return False

class FurrowEvent(object):
    def __init__(self,
                 # or should this be a field type? tricky
                 distance_from_furrow:float,
                 field_types:dict,
                 run):
        """
        A FurrowEvent represents a process that happens in the furrow.

        :param distance_from_furrow: the distance (in number of cell radii) of
        this process from the furrow's frontier. The higher this distance,
        the longer it takes for this event to start walking across the epithelium.

        :param field_types: a map from strings to FieldTypes detailing the parameters
        of the event. These are used to dynamically generate fields in the GUI.

        :param run: A function: (FieldTypes, Epithelium, [Cell])->None. Specifies
        the event's biological logic. Each time the furrow steps across the epithelium,
        this function is run on the subset of cells that the furrow is visiting, adjusted
        for the event's distance from the furrow.
        """
        self.distance_from_furrow = distance_from_furrow
        self.field_types = field_types
        self.run = run

    def __call__(self, furrow_last_position:float, furrow_position:float, epithelium):
        """
        Run the event's biological logic on the subset of cells between
        the furrow's last and current position, adjusting for the event's
        distance from the furrow's frontier.
        """
        left_bound = furrow_position + self.distance_from_furrow
        right_bound = furrow_last_position + self.distance_from_furrow
        cells = epithelium.cell_collision_handler.cells_between(left_bound, right_bound)
        self.run(self.field_types, epithelium, cells)

## Specific Furrow Events

def runR8Selector(field_types, epithelium, cells):
    r8_exclusion_radius = field_types['r8_exclusion_radius'].value
    for cell in cells:
        neighbors = epithelium.neighboring_cells(cell, r8_exclusion_radius)
        assign = True
        for neighbor in neighbors:
            if neighbor.photoreceptor_type == PhotoreceptorType.R8:
                assign = False
        if assign:
            cell.photoreceptor_type = PhotoreceptorType.R8

R8SelectionEvent = FurrowEvent(distance_from_furrow = 0,
                               field_types = {'r8_exclusion_radius' : Integer(4)},
                               run = runR8Selector)

## All Furrow Events ordered from first to last
FurrowEvents = [R8SelectionEvent]
