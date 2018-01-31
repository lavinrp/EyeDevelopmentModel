class FurrowEvent(object):
    def __init__(self,
                 # or should this be a field type? tricky
                 distance_from_furrow: float,
                 field_types: dict,
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
