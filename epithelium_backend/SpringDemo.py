from epithelium_backend.Cell import Cell
from epithelium_backend.PhotoreceptorType import PhotoreceptorType
from epithelium_backend import R8Selector
from epithelium_backend import Furrow
from epithelium_backend import Epithelium
import matplotlib.pyplot as plt
import random as random

def plot(cells, name, grid=5):
    """Plot the cells as circles as a png named `name`"""
    circles = []
    for cell in cells:
        (x,y,z) = cell.position
        c = plt.Circle((x, y), cell.radius, color='b', fill=cell.photoreceptor_type==PhotoreceptorType.R8)
        circles.append(c)
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5,10.5)
    ax.set_xlim(-1*grid, grid)
    ax.set_ylim(-1*grid, grid)
    for c in circles:
        ax.add_artist(c)
    fig.savefig(name, dpi=75)

def demo():
    epithelium = Epithelium.Epithelium(1000)
    # plot(epithelium.cells, 'im/before0.png', 6)
    furrow_start = max(epithelium.cells, key=lambda c: c.position[0]).position[0]
    r8Selector = R8Selector.R8Selector(0,6*0.2)
    furrow = Furrow.Furrow(furrow_start, 0.2, 0.2, [r8Selector])
    for i in range(0,5):
        furrow.update(epithelium)
        plot(epithelium.cells, 'im/before'+str(i)+'.png', 6)

# random.seed(58293)
# # Generate 100 random cells about the origin with radii between 0.1 and 0.35
# cells = [Cell( (random.random()-0.5, random.random()-0.5, 0),
#                (0.2+(random.random()/2))/2)
#          for i in range(0,100)]

# # Plot the cells as they were spawned
# plot(cells, 'before.png')
# # Decompact 250 times with kind of arbitrary parameters
# decompact(cells, iterations=250, spring_constant=8, escape=1.05, dt=0.1)
# # Plot the cells after being decompacted
# plot(cells, 'after.png')
