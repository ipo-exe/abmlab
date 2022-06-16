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
from backend import get_seed, get_window_ids, drop_center_cell
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def beat(i):
    global grd, vct_rows_ids, vct_cols_ids
    grd = conway.compute_next(grd=grd, vct_rows_ids=vct_rows_ids, vct_cols_ids=vct_cols_ids)
    ax1.clear()
    plt.imshow(grd, cmap='Greys_r')
    plt.axis('off')

# define parameters
n_grid = 60
r_density = 0.3

# set random state
n_seed = get_seed()
np.random.seed(n_seed)

# initiate grid
#grd = np.array(1 * (np.random.random(size=(n_grid, n_grid)) < r_density), dtype='int8')
grd = conway.gosper_gun(n_grid=n_grid)  # glider gun
#grd = conway.infinte_pattern(n_grid=n_grid)

# get window paramters
n_rows = len(grd)
n_cols = len(grd[0])
vct_rows_ids, vct_cols_ids = get_window_ids(n_rows=n_rows, n_cols=n_cols, n_rsize=1, b_flat=True)
vct_rows_ids, vct_cols_ids = drop_center_cell(vct_window_rows=vct_rows_ids, vct_window_cols=vct_cols_ids)

# animate
plt.style.use('dark_background')
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(fig, func=beat, interval=10)
plt.show()