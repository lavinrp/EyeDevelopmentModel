from math import inf

class FurrowEvent(object):
    def __init__(self,
                 field_types:dict,
                 run, # type hint for a function?
                 distance_from_furrow:float = 0,
    ):
        self.distance_from_furrow = distance_from_furrow
        self.last_x = inf
        self.field_types = field_types
        self.run = run

    def __call__(self, furrow_position:float, epithelium):
        left_bound = furrow_position + self.distance_from_furrow
        cells = epithelium.cell_collision_handler.cells_between(left_bound, self.last_x)
        self.run(epithelium, cells)
        self.last_x = left_bound
