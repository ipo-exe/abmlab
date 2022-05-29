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
from backend import create_rundir, get_window, status

def gosper_gun(n_grid=60):
    lst_gun = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0],
                [0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	1,	1,	0,	0,	0,	0,	1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]
    grd_gun = np.array(lst_gun, dtype='uint8')
    grd_full = np.zeros(shape=(n_grid, n_grid), dtype='uint8')
    grd_full[1: len(grd_gun) + 1, 1:len(grd_gun[0]) + 1] = grd_gun
    return grd_full

def infinte_pattern(n_grid=60):
    lst_gun = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
               [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grd_gun = np.array(lst_gun, dtype='uint8')
    grd_full = np.zeros(shape=(n_grid, n_grid), dtype='uint8')
    row_i = 20
    col_j = 20
    grd_full[row_i: row_i + len(grd_gun), col_j:col_j+ len(grd_gun[0])] = grd_gun
    return grd_full

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


def play(grd_start, n_gens, n_grid=100, trace=True):
    # simulation object
    dct_out = {'Start': grd_start.copy()}
    # set extra variables
    if trace:
        grd3_traced = np.zeros(shape=(n_gens, n_grid, n_grid), dtype='uint8')
    for i in range(1, n_gens):
        status('step {}'.format(i))
        if trace:
            grd3_traced[i] = grd_start.copy()
        # compute next
        grd_start = compute_next(grd=grd_start)
    # output
    dct_out['End'] = grd_start.copy()
    if trace:
        dct_out['Evolution'] = grd3_traced
    return dct_out

