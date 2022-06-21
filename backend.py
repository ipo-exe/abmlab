'''

Backend routines source code

Copyright (C) 2022 Iporã Brito Possantti

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
import pandas as pd


def drop_center_cell(vct_window_rows, vct_window_cols):
    """
    Remove the center cell for window vectors
    :param vct_window_rows: 1d numpy array of window row ids
    :param vct_window_cols: 1d numpy array of window cols ids
    :return: 1d numpy array (rows), 1d numpy array (cols)
    """
    lst_aux_rows = list()
    lst_aux_cols = list()
    for i in range(len(vct_window_rows)):
        if vct_window_rows[i] == 0 and vct_window_cols[i] == 0:
            pass
        else:
            lst_aux_rows.append(vct_window_rows[i])
            lst_aux_cols.append((vct_window_cols[i]))
    return np.array(lst_aux_rows, dtype='uint16'), np.array(lst_aux_cols, dtype='uint16')


def get_window_ids(n_rows, n_cols, n_rsize=1, b_flat=True):
    """
    Get window cell base indices
    :param n_rows: int number of grid row
    :param n_cols: int number of grid cols
    :param n_rsize: int radius size in cell count
    :param b_flat: boolean to compute flat window
    :return: row indices and column indices
    """
    n_radius = n_rsize
    # get distance vector
    vct_distance = np.arange(start=-n_radius, stop=n_radius + 1)
    # get the base window vector
    vct_window_base = vct_distance % n_cols
    # generate grid for rows
    lst_aux = list()
    for r in range(len(vct_window_base)):
        lst_aux.append(vct_window_base[r] * np.ones(shape=np.shape(vct_window_base)))
    grd_window_rows = np.array(lst_aux, dtype='uint16')
    # generate grid for cols
    lst_aux = list()
    for r in range(len(vct_window_base)):
        lst_aux.append(vct_window_base)
    grd_window_cols = np.array(lst_aux, dtype='uint16')
    if b_flat:
        vct_window_rows = grd_window_rows.flatten()
        vct_window_cols = grd_window_cols.flatten()
        return vct_window_rows, vct_window_cols
    else:
        return grd_window_rows, grd_window_cols


def timestamp(s_sep='-'):
    """
    Generates a string timestamp
    :param s_sep: string separator
    :return: string timestamp
    """
    import datetime
    def_now = datetime.datetime.now()
    yr = def_now.strftime('%Y')
    mth = def_now.strftime('%m')
    dy = def_now.strftime('%d')
    hr = def_now.strftime('%H')
    mn = def_now.strftime('%M')
    sg = def_now.strftime('%S')
    def_lst = [yr, mth, dy, hr, mn, sg]
    def_s = str(s_sep.join(def_lst))
    return def_s


def get_seed():
    """
    Get seed from computer clock
    :return: int
    """
    import datetime
    def_now = datetime.datetime.now()
    hr = def_now.strftime('%H')
    mn = def_now.strftime('%M')
    sg = def_now.strftime('%S')
    return int(sg + mn + hr)


def create_rundir(label='', wkplc='C:'):
    """
    Create a run directory
    :param label: string label
    :param wkplc: string folder path
    :return: string path to directory
    """
    dir_nm = wkplc + '/' + label + '_' + timestamp()
    os.mkdir(dir_nm)
    return dir_nm


def status(msg='Status message', process=True):
    """
    status message routine
    :param msg: string message
    :param process: boolean to denote process
    :return: none
    """
    if process:
        print('\t>>> {:60}...'.format(msg))
    else:
        print('\n\t>>> {:60}\n'.format(msg))



