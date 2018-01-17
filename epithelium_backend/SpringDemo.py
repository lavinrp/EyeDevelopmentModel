import matplotlib.pyplot as plt

def plot(cells, name, grid=5):
    """Plot the cells as circles as a png named `name`"""
    circles = []
    for cell in cells:
        (x,y,z) = cell.position
        c = plt.Circle((x, y), cell.radius, color='b', fill=False)
        circles.append(c)
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5,10.5)
    ax.set_xlim(0, 2*grid)
    ax.set_ylim(0, 2*grid)
    for c in circles:
        ax.add_artist(c)
    fig.savefig(name, dpi=75)
