'''

Conway Game of Life source code

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

import os

import numpy as np
from out import export_gif
from backend import create_rundir, get_window


def compute_next(grd):
    # copy current array
    m_next = grd.copy()
    # scanning loop
    for i in range(len(grd)): # rows
        for j in range(len(grd[i])): # columns

            # get window dict coordinates
            dw = get_window(lcl_i=i, lcl_j=j, size_i=len(grd), size_j=len(grd[i]))

            # define indexed window map object
            dct_w = {'0': grd[dw['nw']['y']][dw['nw']['x']],
                     '1': grd[dw['n']['y']][dw['n']['x']],
                     '2': grd[dw['ne']['y']][dw['ne']['x']],
                     '3': grd[dw['w']['y']][dw['w']['x']],
                     '4': grd[dw['e']['y']][dw['e']['x']],
                     '5': grd[dw['sw']['y']][dw['sw']['x']],
                     '6': grd[dw['s']['y']][dw['s']['x']],
                     '7': grd[dw['se']['y']][dw['se']['x']]}

            # define flat window array
            window = np.array([dct_w['0'],
                               dct_w['1'],
                               dct_w['2'],
                               dct_w['3'],
                               dct_w['4'],
                               dct_w['5'],
                               dct_w['6'],
                               dct_w['7']
                               ])

            # apply rules
            window_sum = np.sum(window)
            # live cell
            if grd[i][j] == 1:
                if window_sum == 2 or window_sum == 3:
                    m_next[i][j] = 1
                else:
                    m_next[i][j] = 0
            else:
                if window_sum == 3:
                    m_next[i][j] = 1
    return m_next


def play(grd_int, n_gens, n_grid=100):
    grid = np.zeros(shape=(n_gens, n_grid, n_grid), dtype='int8')
    grid[0] = grd_int
    for i in range(1, len(grid)):
        grid[i] = compute_next(grd=grid[i - 1])
    return grid


def run_rand(n_gens, n_grid, wkpl='C:/bin', keep_frames=True, r_density=0.1, n_seed=666):
    dir_out = create_rundir(label='CGL', wkplc=wkpl)
    dir_frames = os.mkdir('{}/frames'.format(dir_out))
    np.random.seed(n_seed)
    grd_ini = np.array(1 * (np.random.random(size=(n_grid, n_grid)) < r_density), dtype='int8')
    grd_run = play(grd_ini, n_gens, n_grid)
    # export
    plt.style.use('dark_background')
    for i in range(len(grd_run)):
        plt.imshow(grd_run[i], cmap='Greys_r')
        plt.savefig('{}/CGL_{}.png'.format(dir_frames, str(i).zfill(4)))
        plt.close()
    export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')

