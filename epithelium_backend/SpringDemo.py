from epithelium_backend.Cell import Cell
from epithelium_backend.Epithelium import Epithelium
import matplotlib.pyplot as plt
import random as random

def plot(cells, name, grid=5):
    """Plot the cells as circles as a png named `name`"""
    circles = []
    for cell in cells:
        (x,y,z) = cell.position
        c = plt.Circle((x, y), cell.radius, color='b', fill=False)
        circles.append(c)
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5,10.5)
    ax.set_xlim(-1*grid, grid)
    ax.set_ylim(-1*grid, grid)
    for c in circles:
        ax.add_artist(c)
    fig.savefig(name, dpi=75)

    random.seed(58293)
    # Generate 100 random cells about the origin with radii between 0.1 and 0.35

    testEpithelium = Epithelium(cell_quantity=100, cell_radius_divergence=.4)
