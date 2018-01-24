from math import inf
from epithelium_backend.PhotoreceptorType import PhotoreceptorType

class FieldType(object):
    def __init__(self,
                 value,
                 description = ''):
        self.value = value
        self.description = description

    def validate(self, new_val):
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
                 run): # type hint for Fn?
        self.distance_from_furrow = distance_from_furrow
        self.last_x = inf
        self.field_types = field_types
        self.run = run


    def __call__(self, furrow_position:float, epithelium):
        left_bound = furrow_position + self.distance_from_furrow
        cells = epithelium.cell_collision_handler.cells_between(left_bound, self.last_x)
        self.run(self.field_types, epithelium, cells)
        self.last_x = left_bound

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
                               field_types = {'r8_exclusion_radius' : Integer(0)},
                               run = runR8Selector)

FurrowEvents = [R8SelectionEvent]
