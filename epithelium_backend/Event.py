from math import inf

class Event(object):
    def __init__(self, distance_from_furrow:float = 0):
        self.distance_from_furrow = distance_from_furrow
        self.last_x = inf

    def run(self, furrow_position:float, epithelium):
        left_bound = furrow_position + self.distance_from_furrow
        cells = epithelium.cell_collision_handler.cells_between(left_bound, self.last_x)
        self(epithelium, cells)
        self.last_x = left_bound
