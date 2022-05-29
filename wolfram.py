'''

8-bit Wolfram Celluar Automata source code

Copyright (C) 2022 Iporã Brito Possantti

References:
https://mathworld.wolfram.com/ElementaryCellularAutomaton.html

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

import numpy as np
import matplotlib.pyplot as plt

def pattern8():
    """
    get the Wolfram pattern of 8
    :return:
    """
    p = np.array([[1, 1, 1],
                  [1, 1, 0],
                  [1, 0, 1],
                  [1, 0, 0],
                  [0, 1, 1],
                  [0, 1, 0],
                  [0, 0, 1],
                  [0, 0, 0]])
    return p


def binary(scalar, nlen=8):
    """

    :param scalar: int number
    :param nlen: int length
    :return:
    """
    lst_bin = list(bin(scalar))[2:]
    vct_bin = np.zeros(nlen)
    if len(lst_bin) <= 8:
        vct_bin[nlen - len(lst_bin):] = lst_bin
    return vct_bin


def rule8(num):
    """
    generate a Wolfram rule
    :param num: int rule number
    :return: rule dictionary
    """
    vct_bin = binary(num)
    grd_pat = pattern8()
    dct_rule = dict()
    for i in range(len(vct_bin)):
        dct_rule[str(grd_pat[i])] = vct_bin[i]
    return dct_rule


def compute_next(grd_current, rule):
    """
    Wolfram automaton iteration
    :param grd_current:
    :param rule:
    :return:
    """
    grd_next = np.zeros(len(grd_current), dtype=int)
    for i in range(len(grd_current)):
        if i == 0:
            bottom = len(grd_current) - 1
            upper = i + 1
        elif i == len(grd_current) - 1:
            bottom = i - 1
            upper = 0
        else:
            bottom = i - 1
            upper = i + 1
        lcl_pat = np.array([grd_current[bottom], grd_current[i], grd_current[upper]])
        grd_next[i] = rule[str(lcl_pat)]
    return grd_next


def play(vct_start, n_gens, n_rule=30):
    n_grid = len(vct_start)
    dct_rule = rule8(n_rule)
    grid = np.zeros(shape=(n_gens, n_grid), dtype='uint8')
    grid[0] = vct_start
    for i in range(1, len(grid)):
        grid[i] = compute_next(grd_current=grid[i - 1], rule=dct_rule)
    return grid
