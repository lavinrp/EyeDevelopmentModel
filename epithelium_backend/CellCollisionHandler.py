# Inspired by http://paulbourke.net/miscellaneous/particle/

from math import sqrt
import time as time
from epithelium_backend.Cell import Cell

def distance(tup1: tuple, tup2: tuple) -> float:
    (x1, y1, z1) = tup1
    (x2, y2, z2) = tup2
    x = (x1-x2)
    y = (y1-y2)
    return sqrt(x*x+y*y)


class CellCollisionHandler(object):
    def __init__(self,
                 cells : list,
                 neighbor_escape : float = 3.0,
                 force_escape: float = 1.05,
                 allow_overlap: float=0.95,
                 spring_constant: float = 0.32):

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

        We maintain an undirected graph where each node is a cell and an edge
        connects two nodes if the cells are sufficiently close to potentially
        exert forces on each other. Computing forces is linear in the number
        of edges, and this graph tends to be sparse. Tests have found
        the mean and mode number of edges per node to be about 30.

        We compute this graph on initialization (quadratic re: nodes),
        and the position each cell was at when we determined its neighbors.
        Before computing forces for each cell, we check if a cell has moved
        more than its radius in distance since we last computed its neighbors.
        If so, we recompute its neighbors, but consider only its old neighbors
        and the neighbors of its neighbor that it's now closest to.
        So, when recomputing neighbors for a given cell, we only need to
        consider a tiny fraction of all the cells in the sheet. Because
        the graph is undirected, a cell's neighbors can still change
        even if it never moves much, since cells that move close to it
        will create undirected edges.


        :param cells: the list of cells to track.
        :param neighbor_escape: determines distance at which cells are
           tracked as neighbors of each other. A multiplier of the
           sum of cell radii, not a unit of distance. Used when (re)computing
           neighbors.
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
        # Constants
        self.neighbor_escape = neighbor_escape
        self.force_escape = force_escape
        self.spring_constant = spring_constant
        self.allow_overlap = allow_overlap

        # Maintaing the graph
        self.neighbors = {}
        self.last_position = {}

        # Compute neighbors for the first time
        self.compute_neighbors(cells)

    def register(self, cell: Cell) -> None:
        """
        Add a cell to the graph.
        """
        self.neighbors[cell] = set()
        self.last_position[cell] = cell.position

    def make_edge(self, cell1: Cell, cell2: Cell) -> None:
        """
        Create an undirected edge between the two cells.
        """
        if cell1 != cell2:
            self.neighbors[cell1].add(cell2)
            self.neighbors[cell2].add(cell1)

    def delete_edge(self, cell1: Cell, cell2: Cell) -> None:
        """
        Delete an undirected edge between the two cells.
        """
        self.neighbors[cell1].remove(cell2)
        self.neighbors[cell2].remove(cell1)

    def recompute_neighbors(self, cell: Cell) -> None:
        """
        Update a cell's neighbors. Potential new neighbors are selected from
        the cell's old neighbors and current neighbors of the cell's nearest
        neighbor.
        """
        candidates = set()
        old_neighbors = list(self.neighbors[cell])
        closest_neighbor = min(old_neighbors, key = lambda n : distance(n.position, cell.position))
        for n in old_neighbors:
            candidates.add(n)
            self.delete_edge(cell, n)
        candidates.union(self.neighbors[closest_neighbor])
        for n in candidates:
            if distance(n.position, cell.position) < self.neighbor_escape * (cell.radius + n.radius):
                self.make_edge(cell, n)
        self.last_position[cell] = cell.position

    def recompute_all_neighbors(self) -> None:
        """
        Check if each cell has moved more than its radius in distance since
        we last computed its neighbors. If it has, recompute its neighbors.
        """
        for cell,last_position in self.last_position.items():
            if distance(cell.position, last_position) > cell.radius:
                self.recompute_neighbors(cell)

    def compute_neighbors(self, cells: list) -> None:
        """
        Create the neighbor graph from a list of cells. Quadratic in len(cells)
        """
        for c in cells:
            self.register(c)
        for i in range(0, len(cells)):
            c1 = cells[i]
            for j in range(i, len(cells)):
                c2 = cells[j]
                if distance(c1.position, c2.position)  < self.neighbor_escape * (c1.radius + c2.radius):
                    self.make_edge(c1, c2)


    def decompact(self):
        """
        Push overlapping cells apart, with a tendency to keep them barely overlapping.

        """
        # I've broken with the physics of real springs here by
        # disregarding velocity and mass. As a result, force is equal
        # to the change in the position.  There "should" be a
        # cumulative velocity that affects the forces cells exert on
        # each and their change in position. However, This behavior
        # doesn't model cells very well, because when two cells have
        # pushed apart and stopped colliding, we'd like them to stop
        # moving, not to continue to move apart with high velocities.
        self.recompute_all_neighbors()
        # This actually results in a non-trivial speed up because
        # resolving local variables is faster than resolving
        # member variables.
        allow_overlap = self.allow_overlap
        spring_constant = self.spring_constant
        force_escape = self.force_escape
        for cell, neighbors in self.neighbors.items():
            (cx, cy, cz) = cell.position
            # Using three numbers instead of a tuple doubles the speed
            # because it avoids a lot of needless memory allocations
            # and garbage collection.
            next_x = cx
            next_y = cy
            next_z = cz
            for n in neighbors:
                (nx, ny, nz) = n.position
                cxnx = cx-nx
                cyny = cy-ny
                cznz = cz-nz
                dist = sqrt(cxnx*cxnx + cyny*cyny)
                # Use Hooke's Law. Cells exert pushing forces on each
                # other when they're colliding and pulling forces when
                # there's empty space between them but they're sufficiently
                # close. Force decreases linearly with distance between cells.
                rest_length = allow_overlap * (cell.radius + n.radius)
                if dist <= force_escape * rest_length:
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
                    s = (spring_constant*(dist-rest_length)/dist)
                    next_x -= s*cxnx
                    next_y -= s*cyny
                    next_z -= s*cznz
            cell.next_position = (next_x, next_y, next_z)
        for cell,_ in self.neighbors.items():
            cell.position = cell.next_position
