from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend.Event import Event

class R8Selector(Event):
    def __init__(self,
                 distance_from_furrow:float,
                 r8_exclusion_radius:float):
        super().__init__(distance_from_furrow)
        self.r8_exclusion_radius = r8_exclusion_radius

    def __call__(self, epithelium, cells):
        for cell in cells:
            neighbors = epithelium.cell_collision_handler.cells_within_distance(cell, self.r8_exclusion_radius)
            neighbor_types = set(map(lambda c: c.photoreceptor_type, neighbors))
            if PhotoreceptorType.R8 not in neighbor_types:
                cell.photoreceptor_type = PhotoreceptorType.R8
