from eye_development_gui.FieldType import IntegerFieldType


class FurrowEvent(object):
    def __init__(self,
                 name: str,
                 # or should this be a field type? tricky
                 distance_from_furrow: float,
                 field_types: dict,
                 run):
        """
        A FurrowEvent represents a process that happens in the furrow.

        :param name: The name for this event that will be displayed in the GUI.

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

        self.__distance_from_furrow_key = "distance from furrow"
        self.name = name
        self.last_processed = set()
        self.field_types = field_types
        self.field_types[self.__distance_from_furrow_key] = IntegerFieldType(distance_from_furrow)
        self.run = run
        self.name = name

    def __call__(self, furrow_last_position:float, furrow_position:float, epithelium):
        """
        Run the event's biological logic on the subset of cells between
        the furrow's last and current position, adjusting for the event's
        distance from the furrow's frontier.
        """
        # The Furrow moves from right to left, so left_bound < right_bound.
        left_bound = furrow_position + self.distance_from_furrow
        right_bound = furrow_last_position + self.distance_from_furrow
        # We get the last right_bound because the cell collision handler may have
        # pushed a cell beyond the furrow point. For example, if | is the furrow line
        # and A,B,C,D are cells:
        #
        # initial:        A    B  |  C  D
        # furrow steps:   A  | B     C  D   , processing B
        # decompaction:      |AB     C  D   , A is pushed to right of furrow line
        #
        # So, we need to maintain the set of the cells processed on the last furrow step
        # (self.last_processed), and remove those (set difference) from the union of the current
        # furrow slice and last furrow slice, thereby ensuring that no cell escapes the furrow.
        last_right_bound = right_bound + (right_bound - left_bound)
        candidates = epithelium.cell_collision_handler.cells_between(left_bound, last_right_bound)
        self.last_processed = set(candidates) - self.last_processed
        self.run(self.field_types, epithelium, self.last_processed)

    @property
    def distance_from_furrow(self):
        return self.field_types[self.__distance_from_furrow_key].value

    @distance_from_furrow.setter
    def distance_from_furrow(self, value):
        field = self.field_types[self.__distance_from_furrow_key]  # type: IntegerFieldType
        if field.validate(value):
            field.value = value
