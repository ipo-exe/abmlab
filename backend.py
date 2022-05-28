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


def get_window(lcl_i, lcl_j, size_i, size_j):
    """
    Get window for infinite world
    :param lcl_i: int row index
    :param lcl_j: int column index
    :param size_i: int row size
    :param size_j: int column size
    :return: dict
    """
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



