'''

Conway Game of Life live mode source code

Copyright (C) 2022 Iporã Brito Possantti

References:


************ GNU GENERAL PUBLIC LICENSE ************

https://www.gnu.org/licenses/gpl-3.0.en.html

Permissions:
 - Commercial use
 - Distribution
 - Modification
 - Patent use
 - Private use

Conditions:
 - Disclose source
 - License and copyright notice
 - Same license
 - State changes

Limitations:
 - Liability
 - Warranty

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
import conway
from backend import get_seed
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def beat(i):
    global grd
    grd = conway.compute_next(grd=grd)
    ax1.clear()
    plt.imshow(grd, cmap='Greys_r')
    plt.axis('off')

# define parameters
n_grid = 60
r_density = 0.3

# set random state
n_seed = get_seed()
print(n_seed)
np.random.seed(n_seed)

# initiate grid
grd = np.array(1 * (np.random.random(size=(n_grid, n_grid)) < r_density), dtype='int8')

# animate
plt.style.use('dark_background')
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(fig, func=beat, interval=10)
plt.show()