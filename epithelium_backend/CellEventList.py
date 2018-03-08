from epithelium_backend import Cell


def passive_growth(cell: Cell):
    """
    If this cell's radius is at least the maximum radius for a cell, then calls spawn_new_cell. Otherwise, it will
    grow by the cell's growth rate.
    :return:
    """
    # Check if cell is large enough to divide
    if cell.radius >= cell.max_radius:
        return cell.divide()
    else:
        # If not large enough, grow the cell a little bit for next time
        cell.grow_cell(cell.growth_rate)
        return None
