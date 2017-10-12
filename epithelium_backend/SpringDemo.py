from epithelium_backend.Cell import Cell
from epithelium_backend.SpringSimulator import decompact
# pip install matplotlib
import matplotlib.pyplot as plt
import random as random

def plot(cells, name):
    """Plot the cells as circles as a png named `name`"""
    circles = []
    for cell in cells:
        (x,y,z) = cell.position
        c = plt.Circle((x, y), cell.radius, color='b', fill=False)
        circles.append(c)
    fig, ax = plt.subplots()
    ax.set_xlim((-3, 3))
    ax.set_ylim((-3, 3))
    for c in circles:
        ax.add_artist(c)
    fig.savefig(name)

random.seed(58293)
# Generate 100 random cells about the origin with radii between 0.1 and 0.35
cells = [Cell( (random.random()-0.5, random.random()-0.5, 0),
               (0.2+(random.random()/2))/2)
         for i in range(0,100)]

# Plot the cells as they were spawned
plot(cells, 'before.png')
# Decompact 250 times with kind of arbitrary parameters
decompact(cells, iterations=250, spring_constant=8, escape=1.05, dt=0.1)
# Plot the cells after being decompacted
plot(cells, 'after.png')
