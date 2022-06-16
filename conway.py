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
from backend import create_rundir, get_window_ids, drop_center_cell, status

def gosper_gun(n_grid=60):
    """
    Return a gosper gun pattern inside a grid
    :param n_grid: int grid size n x n
    :return: 2d numpy array
    """
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
    """
    Retuns an infinite pattern seed inside a grid
    :param n_grid: int grid size n x n
    :return: 2d numpy array
    """
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


def compute_next(grd, vct_rows_ids, vct_cols_ids):
    """
    Conway Game of Life step function
    :param grd: 2d numpy array start grid
    :param vct_rows_ids: 1d numpy array base window row vector
    :param vct_cols_ids: 1d numpy array base window cols vector
    :return: 2d numpy array next grid
    """
    # copy current array
    m_next = grd.copy()
    # get parameters
    n_rows = len(grd)
    n_cols = len(grd[0])
    # scanning loop
    for i in range(n_rows): # rows
        for j in range(n_cols): # columns
            vct_window = grd[(i + vct_rows_ids) % n_rows, (j + vct_cols_ids) % n_cols]
            # apply rules
            window_sum = np.sum(vct_window)
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


def play(grd_start, n_gens, trace=True):
    """
    Run the CGL model
    :param grd_start: 2d numpy array start squared grid
    :param n_gens: int number of generations
    :param trace: boolean to trace back all generations
    :return: output dict
    """
    # simulation object
    dct_out = {'Start': grd_start.copy()}
    # get window paramters
    n_rows = len(grd_start)
    n_cols = len(grd_start[0])
    vct_rows_ids, vct_cols_ids = get_window_ids(n_rows=n_rows, n_cols=n_cols, n_rsize=1, b_flat=True)
    vct_rows_ids, vct_cols_ids = drop_center_cell(vct_window_rows=vct_rows_ids, vct_window_cols=vct_cols_ids)
    # set extra variables
    if trace:
        grd3_traced = np.zeros(shape=(n_gens, len(grd_start), len(grd_start)), dtype='uint8')
    # main loop
    for i in range(1, n_gens):
        status('step {}'.format(i))
        if trace:
            grd3_traced[i] = grd_start.copy()
        # compute next
        grd_start = compute_next(grd=grd_start,
                                 vct_rows_ids=vct_rows_ids,
                                 vct_cols_ids=vct_cols_ids)
    # output
    dct_out['End'] = grd_start.copy()
    if trace:
        dct_out['Evolution'] = grd3_traced
    return dct_out

