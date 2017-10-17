# Inspired by http://paulbourke.net/miscellaneous/particle/
# but simpler and more naive

from math import sqrt
from epithelium_backend.Cell import Cell

# Vector functions on tuples
# Sorry to reimplement the wheel; but only 20 lines.
def distance(cell1: Cell, cell2: Cell) -> float:
    (x1, y1, z1) = cell1.position
    (x2, y2, z2) = cell2.position
    return sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


def minus(tup1: tuple, tup2: tuple) -> tuple:
    (x1, y1, z1) = tup1
    (x2, y2, z2) = tup2
    return (x1-x2, y1-y2, z1-z2)

def add(tup1: tuple, tup2: tuple) -> tuple:
    (x1, y1, z1) = tup1
    (x2, y2, z2) = tup2
    return (x1+x2, y1+y2, z1+z2)


def multiply(tup: tuple, c: float) -> tuple:
    (x, y, z) = tup
    return (x*c, y*c, z*c)


# Spring Simulation
def force(cell1: Cell, cell2: Cell, spring_constant: float, escape: float) -> tuple:
    """
    Compute the force on cell1 by cell2 using Hooke's Law.
    Cells exert pushing forces on each other when they're colliding
    and pulling forces when there's empty space between them but they're
    sufficiently close. The force scales linearly with the distance of the
    cells from another.

    :return: The force vector representing cell2's force on cell1.
    """
    dist = distance(cell1, cell2)
    if dist > escape * (cell1.radius + cell2.radius):
        return (0,0,0)
    else:
        rest_length = cell2.radius+cell1.radius
        spring = spring_constant*(dist - rest_length)
        return multiply(minus(cell1.position,cell2.position), -1*spring/dist)


def compute_forces(cells: list, spring_constant: float, escape: float) -> dict:
    """
    Compute the summed force on each cell. Naively quadratic w.r.t. cells.

    :return: a map from each cell to the summed forces on it.
    """
    forces = {cell : (0,0,0) for cell in cells}
    for i in range(0, len(cells)):
        for j in range(i+1, len(cells)):
            force_on_i = force(cells[i], cells[j], spring_constant, escape)
            forces[cells[i]] = add(forces[cells[i]], force_on_i)
            # Newton's 3rd -- the force on j is the negative force on i.
            forces[cells[j]] = add(forces[cells[j]], multiply(force_on_i, -1))
    return forces


def update_positions(cells: list, spring_constant: float, escape: float, dt: float) -> None:
    """
    Compute the summed force on each cell, and use that to compute
    velocities and changes in position. Update the cells' positions.
    """
    forces = compute_forces(cells, spring_constant, escape)
    for cell in cells:
        acceleration = forces[cell] # mass is 1 for simplicity, so f = a.
        # I've broken with the physics of real springs
        # here. Velocity should be cumulative; the new velocity should
        # be the old velocity + acceleration*dt. Also, The force that
        # one cell exerts on another should be partially dependent on
        # the cells' velocities. (It affects the damping part
        # specifically, which I removed.) This behavior doesn't model
        # cells very well though, because when two cells have pushed
        # apart and stopped colliding, we'd like their velocities to
        # be 0, not a large number, because we don't want them to
        # continue moving apart or exert large forcing on the
        # neighbors they're moving into.
        velocity = multiply(acceleration, dt)
        cell.position = add(cell.position, multiply(velocity, dt))


def decompact(cells: list,
              iterations: float = 100,
              spring_constant: float = 2,
              escape: float = 1.05,
              dt:float = 0.1) -> None:
    """
    Push overlapping cells apart, with a tendency to keep them barely overlapping.

    :param cells: A list of cells to push apart
    :param iteration: the number of times to compute and apply forces
    :param spring_constant: determines spring stiffness; linearly correlated
       to the magnitude of the force cells exert on each other.
    :param escape: determines distance at which pulling forces are exerted.
       If escape=1, then cells don't exert any pulling forces. If >1,
       cells exert pulling forces until their distance is greater than
       escape multiplied by the sum of their radii (two cells
       touching have a distance equal to the sum of their radii).
       A small escape, like around 1.05, will mean that cells tend to stick
       togther and overlap maybe a little bit. A large escape tends to make
       cells overlap a lot (since cells would exert non-local pulling forces)
    :param dt: The unit of time over which to assume the force is constant
       in each iteration. Smaller dt leads to better behavior but requires
       more iterations (since cells are moved less with each iteration).
       dt=0.1 is a good trade off; much higher and cells tend to be pushed too
       far apart.
    """
    for i in range(1, iterations):
        update_positions(cells, spring_constant, escape, dt)
