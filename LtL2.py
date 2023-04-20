# Larger than Life Cellular Automata
# Author: Connor McShaffrey

# This is my second (faster) implementation of the Larger than Life cellular automata. 
# It uses the convolution function from scipy.signal to count the number of neighbors
# of each cell. This is much faster than my first implementation, which used nested
# for loops to count the neighbors of each cell.

################################################################################################################

'Imports'

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

################################################################################################################
'Functions'

# Count the number of neighbors of each cell
def count_neighbors(grid, r):
    kernel = np.ones((2 * r + 1, 2 * r + 1))
    kernel[r, r] = 0
    count = convolve2d(grid, kernel, mode='same', boundary='wrap')
    return count

# Update the grid
def update(grid, r, Bmin, Bmax, Smin, Smax):
    neighbors = count_neighbors(grid, r)
    birth = np.logical_and(neighbors >= Bmin, neighbors <= Bmax)
    survival = np.logical_and(neighbors >= Smin - 1, neighbors <= Smax)  # Subtract 1 from Smin as live cells count themselves
    new_grid = np.where(grid == 1, survival, birth).astype(int)
    return new_grid

# Simulate the grid
def simulate(grid, r, Bmin, Bmax, Smin, Smax, steps):
    for _ in range(steps):
        grid = update(grid, r, Bmin, Bmax, Smin, Smax)
    return grid

# Parameters
width, height = 600, 600
r = 8  # Neighborhood size
Bmin, Bmax = 79, 106  # Birth range
Smin, Smax = 79, 137  # Survival range
steps = 50

# Random initial state
initial_grid = np.random.randint(0, 2, size=(height, width))

# Simulation
final_grid = simulate(initial_grid, r, Bmin, Bmax, Smin, Smax, steps)

# Visualization
plt.imshow(final_grid, cmap='binary')
plt.show()
