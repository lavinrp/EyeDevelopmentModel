# Inspired by http://paulbourke.net/miscellaneous/particle/
# but simpler and more naive

from math import sqrt

# Vector functions on tuples
# Sorry to reimplement the wheel; we can refactor later
# I did some cursory googling and didn't find much
def distance(cell1, cell2):
    (x1, y1, z1) = cell1.position
    (x2, y2, z2) = cell2.position
    return sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


def minus(tup1: tuple, tup2: tuple) -> tuple:
    (x1, y1, z1) = tup1
    (x2, y2, z2) = tup2
    return (x1-x2, y1-y2, z1-z2)

def add(tup1, tup2):
    (x1, y1, z1) = tup1
    (x2, y2, z2) = tup2
    return (x1+x2, y1+y2, z1+z2)


def multiply(tup, c):
    (x, y, z) = tup
    return (x*c, y*c, z*c)


# Spring Simulation
def force(cell1, cell2, spring_constant, escape):
    """Compute the force on cell1 by cell2 using Hooke's Law
    The force increases linearly with @spring_constant.

    Cells exert pushing forces on each other when they're colliding
    (c1 and c2 collide when distance(c1,c2) < c1.radius + c2.radius)
    and pulling forces when there's empty space between them.
    @escape determines the distance at which cells stop exerting
    forces on each other; if @escape is 1.0, cells no longer exert
    forces when they've stopped colliding. If it's greater than 1.0,
    they exert pulling forces on each other when close. If less than 1.0,
    they will stop exerting forces on each even when colliding."""
    dist = distance(cell1, cell2)
    if dist > escape * (cell1.radius + cell2.radius):
        return (0,0,0)
    else:
        rest_length = cell2.radius+cell1.radius
        spring = spring_constant*(dist - rest_length)
        return multiply(minus(cell1.position,cell2.position), -1*spring/dist)


def compute_forces(cells, spring_constant, escape):
    """Return a map from cells to the summed forces on them.
    Naively quadratic with the number of cells."""
    forces = {cell : (0,0,0) for cell in cells}
    for i in range(0, len(cells)):
        for j in range(i+1, len(cells)):
            force_on_i = force(cells[i], cells[j], spring_constant, escape)
            forces[cells[i]] = add(forces[cells[i]], force_on_i)
            # Newton's 3rd -- the force on j is the negative force on i.
            forces[cells[j]] = add(forces[cells[j]], multiply(force_on_i, -1))
    return forces


def update_positions(cells, spring_constant, escape, dt):
    """Compute the summed force on each cell and update their positions."""
    forces = compute_forces(cells, spring_constant, escape)
    for cell in cells:
        acceleration = forces[cell] # mass is 1 for simplicity, so f = a
        # I've broken with the physics of real springs here. Velocity should be cumulative;
        # the new velocity should be the old velocity + acceleration*dt. Also,
        # The force that one cell exerts on another should be partially dependent
        # on the cells' velocities. (It affects the damping part specifically,
        # which I removed.) This behavior doesn't model cells very well though,
        # because when two cells have pushed apart and stopped colliding, we'd like
        # their velocities to be 0, not a large number, because we don't want them
        # to continue moving apart.
        velocity = multiply(acceleration, dt)
        cell.position = add(cell.position, multiply(velocity, dt))


def decompact(cells, iterations=100, spring_constant=2, escape=1.05, dt=0.1):
    for i in range(1, iterations):
        update_positions(cells, spring_constant, escape, dt)
