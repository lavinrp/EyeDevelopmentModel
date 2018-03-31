# Inspired by http://paulbourke.net/miscellaneous/particle/


from math import sqrt, ceil
from epithelium_backend.Cell import Cell


def distance(p1, p2):
    (x1,y1,z1) = p1
    (x2,y2,z2) = p2
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


class CellCollisionHandler(object):
    """
    Cells exert pushing and pulling forces on each other. The job
    of the CellCollisionHandler is to efficiently move cells based on
    these forces.

    A given cell only exerts forces on its surrounding neighbors.
    So, if we have a sheet of a thousand cells, every cell affects
    at most a dozen others at one point in time, probably. So,
    a naive quadratic algorithm algorithm that computes forces
    for all pairs of cells will be inefficient, because most cells
    don't affect one another. But, cells move, and the cells that
    another impacts changes over time. If we determine up front
    all the cells that are relevant to a given cell, and efficiently
    maintain this over time, then we can get linear performance.
    For each cell, there's only a constant number of other cells relevant
    to it that we need to consider when computing forces.

    We partition R^2 into a grid of boxes, where each box is a little
    bigger than the average cell diameter, and define a mapping from
    cell positions to the corresponding box. Then, to get the neighbors
    of a cell, we get the coordinates of its box in the grid and do
    simple arithmetic to find its neighboring boxes, and get the cells
    in those boxes. If a cell is in box (i,j) for example, its neighbors
    would be in boxes like (i-1, j-1) (top left), (i, j-1) (left),
    ..., (i+1, j+1) (bottom right).
    The mapping from cell position to grid coordinate takes constant time,
    and is recomputed every time a cell's position changes.
    Decompacting the list of cells is linear w.r.t. the number of cells.

    This grid structure also allows us to get the list of cells within
    a certain distance of another cell in time proportional to the distance.

    :param cells: the list of cells to track.
    :param force_escape: determines distance at which pulling forces are exerted.
       If escape=1, then cells don't exert any pulling forces. If >1,
       cells exert pulling forces until their distance is greater than
       escape multiplied by the sum of their radii (two cells
       touching have a distance equal to the sum of their radii).
       A small escape, like around 1.05, will mean that cells tend to stick
       togther and overlap maybe a little bit. A large escape tends to make
       cells overlap a lot (since cells would exert non-local pulling forces)
    :param allow_overlap: If less than 1, cells exert pulling forces on
       each other when colliding, making them overlap in equilibrium.
    :param spring_constant: determines spring stiffness; linearly correlated
       to the magnitude of the force cells exert on each other.
    """
    def __init__(self,
                 cells: list,
                 force_escape: float = 1.05,
                 allow_overlap: float = 0.95,
                 spring_constant: float = 0.32):
        self.cells = cells
        # Constants
        self.force_escape = force_escape
        self.allow_overlap = allow_overlap
        self.spring_constant = spring_constant

        self.cell_quantity = 0
        self.avg_radius = 0
        self.center_x = 0
        self.center_y = 0
        self.max_grid_size = 0
        self.box_size = 0
        self.dimension = 0
        self.grids = []
        self.non_empty = set()

        self.fill_grid()

    def compute_row(self, y):
        return int(self.dimension/2 + (y-self.center_y)/self.box_size)

    def compute_col(self, x):
        return int(self.dimension/2 + (x-self.center_x)/self.box_size)

    def bin(self, cell: Cell):
        """Compute the row and column of the cell given its position. """
        # Cells at the center should be in the middle of our space.
        # So, we compute the distance of the cell from the center
        # (cell.position_x-self.center_x)
        # find out how many boxes the distance corresponds to
        # (divide by self.box_size)
        # and use that to figure out how many steps left or right
        # to go from the middle
        # (add to self.dimension/2)
        col = self.compute_col(cell.position_x)
        row = self.compute_row(cell.position_y)
        # Map the row,col to an index in our one dimensional grid vector.
        bin = self.dimension*row + col
        if bin >= len(self.grids):
            # Resize the grid and re-bin all the cells.
            self.fill_grid()
            # Because the dimensions and centers have changed,
            # we have to recompute the bin.
            return self.bin(cell)
        return self.dimension*row + col

    def register(self, cell: Cell):
        """Add the cell to the collision handler."""
        cell.next_x = cell.position_x
        cell.next_y = cell.position_y
        cell.bin = self.bin(cell)
        self.grids[cell.bin].append(cell)
        self.non_empty.add(cell.bin)

    def deregister(self, cell: Cell):
        """Remove the cell from the collision handler."""
        self.grids[cell.bin].remove(cell)
        # May want to remove from non_empty

    def fill_grid(self):
        """
        Create or resize the collision handler's grid and
        add every cell to it.
        """
        # Grid
        # Compute the average radius and center so we know how to partition
        # the space.
        self.cell_quantity = len(self.cells)
        self.avg_radius = sum(map(lambda x : x.radius, self.cells))/len(self.cells)
        self.center_x = sum(map(lambda x : x.position_x, self.cells))/len(self.cells)
        self.center_y = sum(map(lambda x : x.position_y, self.cells))/len(self.cells)
        # Twice the maximum x and y coordinates we can handle.
        # Choose a space big enough to hold 4x more cells than we have.
        self.max_grid_size = 2 * sqrt(self.avg_radius**2 * 3.14 * self.cell_quantity)
        # The width of each box. Chosen so that two cells can exert forces
        # on each other only if they're in adjacent boxes.
        self.box_size = self.avg_radius * 2 * self.force_escape

        # The number of rows and columns needed.
        self.dimension = ceil(self.max_grid_size / self.box_size)
        # The one dimensional list representing our grid.
        self.grids = [[] for x in range(0,self.dimension**2)]
        # The set of non-empty boxes -- the only ones we need
        # to examine when decompacting
        self.non_empty = set()

        for cell in self.cells:
            self.register(cell)

    def push_pull(self, cell1: Cell, cell2: Cell):
        """Compute the force of cell1 on cell2 and vice versa."""
        # I've broken with the physics of real springs here by
        # disregarding velocity and mass. As a result, force is equal
        # to the change in the position.  There "should" be a
        # cumulative velocity that affects the forces cells exert on
        # each and their change in position. However, This behavior
        # doesn't model cells very well, because when two cells have
        # pushed apart and stopped colliding, we'd like them to stop
        # moving, not to continue to move apart with high velocities.

        cxnx = cell1.position_x - cell2.position_x
        cyny = cell1.position_y - cell2.position_y
        # If they're on top of each other, they should push each other apart.
        # Distance can't equal zero since we divide by distance later on.
        dist = max(sqrt(cxnx*cxnx + cyny*cyny), self.avg_radius/100)
        # Use Hooke's Law. Cells exert pushing forces on each
        # other when they're colliding and pulling forces when
        # there's empty space between them but they're sufficiently
        # close. Force decreases linearly with distance between cells.
        rest_length = self.allow_overlap * (cell1.radius + cell2.radius)
        if dist <= self.force_escape * rest_length:
            # the difference between the distance and rest_length
            # determines the directionality of the force.
            # If the springs are farther apart than their rest_length,
            # they pull each other together. If closer, they push.
            # So, defining rest_length as the sum of the cells'
            # radii means that they are at equilibrium when their
            # circumfrences are touching. Multiplying the rest_length
            # by allow_overlap means springs will be at equilibrium
            # when overlapping, since it makes the rest_length
            # smaller.
            s = (self.spring_constant*(dist-rest_length)/dist)
            scxnx = s*cxnx
            scyny = s*cyny
            cell1.next_x -= scxnx
            cell1.next_y -= scyny
            cell2.next_x += scxnx
            cell2.next_y += scyny

    def decompact(self):
        """
        Push overlapping cells apart, with a tendency to keep them barely overlapping.

        """
        # This actually results in a non-trivial speed up because
        # resolving local variables is faster than resolving
        # member variables.
        grids = self.grids
        len_grids = len(grids)
        dimension = self.dimension
        for i in self.non_empty:
            box = grids[i]
            right = i+1
            down_left = i+dimension-1
            down = i+dimension
            down_right = i+dimension+1
            for m in range(0, len(box)):
                cell1 = box[m]
                for n in range(m+1, len(box)):
                    cell2 = box[n]
                    self.push_pull(cell1, cell2)

            for cell1 in box:
                for j in [right, down_left, down, down_right]:
                    if 0 < j < len_grids:
                        for cell2 in grids[j]:
                            self.push_pull(cell1, cell2)

        for cell in self.cells:
            cell.x = cell.next_x
            cell.y = cell.next_y
            cell.position_x = cell.next_x
            cell.position_y = cell.next_y
            g = self.bin(cell)
            if g != cell.bin:
                grids[cell.bin].remove(cell)
                grids[g].append(cell)
                cell.bin = g
                self.non_empty.add(g)

    def cells_within_distance(self, cell, r):
        box_number = ceil(r/self.box_size)
        cells = []
        for row in range(-box_number, box_number+1):
            for col in range(-box_number, box_number+1):
                grid = cell.bin + self.dimension*row + col
                if 0 < grid < len(self.grids):
                    cells.extend(self.grids[grid])
        return list(filter(lambda n: distance((cell.position_x, cell.position_y, cell.position_z),
                                              (n.position_x, n.position_y, n.position_z)) <= r, cells))

    def posterior_to_anterior(self):
        for col in range(0, self.dimension):
            for row in range(0, self.dimension):
                for cell in self.grids[self.dimension*row+col]:
                    yield cell

    def cells_between(self, min_x, max_x):
        """
        Return the list of cells between min_x and max_x, sorted from
        posterior to anterior order.
        """
        max_col = min(self.dimension-1, self.compute_col(max_x))
        min_col = max(0, self.compute_col(min_x))
        result = []
        for col in range(min_col, max_col+1):
            for row in range(0,self.dimension):
                for cell in self.grids[self.dimension*row+col]:
                    # The boxes are only an approxiation -- we don't
                    # know for sure that the cell is actually within
                    # the range.
                    if min_x < cell.position_x < max_x:
                        result.append(cell)
        # todo: just walk backwards, from max_col to min_col
        # sort posterior to anterior
        result.sort(key=lambda c: -c.position_x)
        return result
