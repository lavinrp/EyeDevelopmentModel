from epithelium_backend.PhotoreceptorType import PhotoreceptorType

class R8Selector(object):
    def __init__(self, r8_exclusion_radius):
        self.r8_exclusion_radius = r8_exclusion_radius

    def run(self, epithelium, cell):
        neighbors = epithelium.cell_collision_handler.cells_within_distance(cell, self.r8_exclusion_radius)
        neighbor_types = set(map(lambda c: c.photoreceptor_type, neighbors))
        if PhotoreceptorType.R8 not in neighbor_types:
            cell.photoreceptor_type = PhotoreceptorType.R8
