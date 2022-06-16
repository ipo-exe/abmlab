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


def get_window_ids_deprec(vct_full, lcl_i, n_rsize=1):
    """
    get the window ids from a 1-d array
    :param vct_full: 1d numpy array
    :param lcl_i: int cell position
    :param n_rsize: int cell radius size
    :return: 1d numpy array of indexes
    """
    if lcl_i < n_rsize:  # west side
        vct_window_p1_ids = np.arange(start=0, stop=lcl_i + n_rsize + 1, step=1, dtype='uint16')
        vct_window_p2_ids = np.arange(start=len(vct_full) + lcl_i - n_rsize, stop=len(vct_full), step=1, dtype='uint16')
        vct_window_ids = np.concatenate((vct_window_p2_ids, vct_window_p1_ids), axis=None)
    elif lcl_i >= len(vct_full) - n_rsize:  # east side
        vct_window_p1_ids = np.arange(start=lcl_i - n_rsize, stop=len(vct_full), step=1, dtype='uint16')
        vct_window_p2_ids = np.arange(start=0, stop=n_rsize - (len(vct_full) - lcl_i) + 1, step=1, dtype='uint16')
        vct_window_ids = np.concatenate((vct_window_p1_ids, vct_window_p2_ids), axis=None)
    else:  # bulk
        vct_window_ids = np.arange(start=lcl_i - n_rsize, stop=lcl_i + n_rsize + 1, step=1, dtype='uint16')
    return vct_window_ids


def get_window_x(vct_full, lcl_i, n_rsize=1, b_drop_center=False):
    """
    Get the window dataframe for 1D array
    :param vct_full: 1d numpy array
    :param lcl_i: int cell position
    :param n_rsize: int cell radius size
    :param b_drop_center: boolean to drop center cell values from window
    :return: pandas dataframe
    """
    # get ids
    vct_ids = get_window_ids_deprec(vct_full=vct_full, lcl_i=lcl_i, n_rsize=n_rsize)
    # get values
    vct_values = np.take(a=vct_full, indices=vct_ids)
    # create dataframe
    df_window = pd.DataFrame({'Vector_i': vct_ids, 'Value': vct_values})
    # drop center cell
    if b_drop_center:
        df_window.drop(df_window.loc[df_window['Vector_i'] == lcl_i].index, inplace=True)
    return df_window


def get_window_xy_ids( lcl_i, lcl_j, n_rows, n_cols, n_rsize=1, b_drop_center=False):
    n_window_size = 1 + (2 * n_rsize)
    # get rows ids
    vct_grd_rows = np.arange(start=0, stop=n_rows, step=1)
    # get cols ids
    vct_grd_cols = np.arange(start=0, stop=n_cols, step=1)
    # get window rows ids
    vct_rows_ids = get_window_ids_deprec(vct_full=vct_grd_rows, lcl_i=lcl_i, n_rsize=n_rsize)
    grd_window_i = np.zeros(shape=(n_window_size, n_window_size), dtype='uint16')
    grd_window_j = np.zeros(shape=(n_window_size, n_window_size), dtype='uint16')
    # scan rows elements
    for k in range(len(vct_rows_ids)):
        # get window row ids
        vct_row_window_ids = get_window_ids_deprec(vct_full=vct_grd_cols, lcl_i=lcl_j, n_rsize=n_rsize)
        # extract i position (y)
        grd_window_i[k] = vct_rows_ids[k]
        # extract j position (x)
        grd_window_j[k] = vct_row_window_ids
    df_window = pd.DataFrame({'Grid_i': grd_window_i.flatten(),
                              'Grid_j': grd_window_j.flatten()})
    # drop center cell
    if b_drop_center:
        df_window.drop(df_window.loc[(df_window['Grid_i'] == lcl_i) & (df_window['Grid_j'] == lcl_j)].index, inplace=True)
    return df_window


def get_window_xy_deprec(lcl_i, lcl_j, size_i, size_j):
    """
    Get window object for infinite 2d world
    :param lcl_i: int row index
    :param lcl_j: int column index
    :param size_i: int row size
    :param size_j: int column size
    :return: dict
    """
    # start dict
    dct_w = {}
    if lcl_i == 0: # top
        if lcl_j == 0: # top left edge
            dct_w['nw'] = {'y': size_i - 1, 'x': size_j - 1}
            dct_w['n'] = {'y': size_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': size_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': lcl_i + 1, 'x': lcl_j + 1}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': size_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': size_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        elif lcl_j == size_j - 1:  # top right edge
            dct_w['nw'] = {'y': size_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': size_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': size_i - 1, 'x': 0}
            dct_w['e'] = {'y': lcl_i, 'x': 0}
            dct_w['se'] = {'y': lcl_i + 1, 'x': 0}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        else: # top bulk
            dct_w['nw'] = {'y': size_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': size_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': size_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': lcl_i + 1, 'x': lcl_j + 1}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
    elif lcl_i == size_i - 1: # bottom
        if lcl_j == 0: # bottom left edge
            dct_w['nw'] = {'y': lcl_i - 1, 'x': size_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': 0, 'x': lcl_j + 1}
            dct_w['s'] = {'y': 0, 'x': lcl_j}
            dct_w['sw'] = {'y': 0, 'x': size_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': size_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        elif lcl_j == size_j - 1:  # bottom right edge
            dct_w['nw'] = {'y': lcl_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': 0}
            dct_w['e'] = {'y': lcl_i, 'x': 0}
            dct_w['se'] = {'y': 0, 'x': 0}
            dct_w['s'] = {'y': 0, 'x': lcl_j}
            dct_w['sw'] = {'y': 0, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        else: # bottom bulk
            dct_w['nw'] = {'y': lcl_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': 0, 'x': lcl_j + 1}
            dct_w['s'] = {'y': 0, 'x': lcl_j}
            dct_w['sw'] = {'y': 0, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
    else: # bulk
        if lcl_j == 0:  # bulk left edge
            dct_w['nw'] = {'y': lcl_i - 1, 'x': size_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': lcl_i + 1, 'x': lcl_j + 1}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': size_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': size_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        elif lcl_j == size_j - 1:  # bulk right edge
            dct_w['nw'] = {'y': lcl_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': 0}
            dct_w['e'] = {'y': lcl_i, 'x': 0}
            dct_w['se'] = {'y': lcl_i + 1, 'x': 0}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
        else:  # bulk bulk
            dct_w['nw'] = {'y': lcl_i - 1, 'x': lcl_j - 1}
            dct_w['n'] = {'y': lcl_i - 1, 'x': lcl_j}
            dct_w['ne'] = {'y': lcl_i - 1, 'x': lcl_j + 1}
            dct_w['e'] = {'y': lcl_i, 'x': lcl_j + 1}
            dct_w['se'] = {'y': lcl_i + 1, 'x': lcl_j + 1}
            dct_w['s'] = {'y': lcl_i + 1, 'x': lcl_j}
            dct_w['sw'] = {'y': lcl_i + 1, 'x': lcl_j - 1}
            dct_w['w'] = {'y': lcl_i, 'x': lcl_j - 1}
            dct_w['c'] = {'y': lcl_i, 'x': lcl_j}
    return dct_w


def nowsep(p0='-'):
    import datetime
    def_now = datetime.datetime.now()
    yr = def_now.strftime('%Y')
    mth = def_now.strftime('%m')
    dy = def_now.strftime('%d')
    hr = def_now.strftime('%H')
    mn = def_now.strftime('%M')
    sg = def_now.strftime('%S')
    def_lst = [yr, mth, dy, hr, mn, sg]
    def_s = str(p0.join(def_lst))
    return def_s

def get_seed():
    import datetime
    def_now = datetime.datetime.now()
    hr = def_now.strftime('%H')
    mn = def_now.strftime('%M')
    sg = def_now.strftime('%S')
    return int(sg + mn + hr)

def create_rundir(label='', wkplc='C:'):
    dir_nm = wkplc + '/' + label + '_' + nowsep()
    os.mkdir(dir_nm)
    return dir_nm


def status(msg='Status message', process=True):
    if process:
        print('\t>>> {:60}...'.format(msg))
    else:
        print('\n\t>>> {:60}\n'.format(msg))



