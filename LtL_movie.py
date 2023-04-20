import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib import rc

rc('animation', html='html5')

def count_neighbors(grid, r):
    padded_grid = np.pad(grid, ((r, r), (r, r)), mode='wrap')
    count = np.zeros_like(grid)
    
    for i in range(-r, r+1):
        for j in range(-r, r+1):
            if i != 0 or j != 0:
                count += padded_grid[r+i:height+r+i, r+j:width+r+j]
    
    return count

def update(grid, r, Bmin, Bmax, Smin, Smax):
    neighbors = count_neighbors(grid, r)
    birth = np.logical_and(neighbors >= Bmin, neighbors <= Bmax)
    survival = np.logical_and(neighbors >= Smin - 1, neighbors <= Smax)  # Subtract 1 from Smin as live cells count themselves
    new_grid = np.where(grid == 1, survival, birth).astype(int)
    return new_grid

def simulate(grid, r, Bmin, Bmax, Smin, Smax, steps):
    for _ in range(steps):
        grid = update(grid, r, Bmin, Bmax, Smin, Smax)
    return grid

def init():
    im.set_data(np.zeros((height, width)))
    return [im]

def animate(i):
    im.set_data(grids[i])
    return [im]

# Parameters
width, height = 400, 400
r = 10  # Neighborhood size
Bmin, Bmax = 123, 170  # Birth range
Smin, Smax = 123, 212  # Survival range
steps = 100

# Random initial state
initial_grid = np.random.randint(0, 2, size=(height, width))

# Simulation
grids = [initial_grid]
for _ in range(steps):
    grids.append(update(grids[-1], r, Bmin, Bmax, Smin, Smax))

# Animation
fig, ax = plt.subplots()
im = ax.imshow(grids[0], cmap='binary', animated=True)
ani = FuncAnimation(fig, animate, init_func=init, frames=steps, blit=True, interval=100)

# Save the animation as a GIF
ani.save('animation.gif', writer='pillow', fps=10)
