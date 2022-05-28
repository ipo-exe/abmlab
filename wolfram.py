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
    get the wolfram pattern of 8
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


def binary(scalar, vlen=8):
    lst_bin = list(bin(scalar))[2:]
    v_bin = np.zeros(vlen)
    if len(lst_bin) <= 8:
        v_bin[vlen - len(lst_bin) : ] = lst_bin
    return v_bin


def rule8(num):
    n_bin = binary(num)
    pat = pattern8()
    dct_rule = dict()
    for i in range(len(n_bin)):
        dct_rule[str(pat[i])] = n_bin[i]
    return dct_rule


def next(current, rule):
    next = np.zeros(len(current), dtype=int)
    for i in range(len(current)):
        if i == 0:
            bottom = len(current) - 1
            upper = i + 1
        elif i == len(current) - 1:
            bottom = i - 1
            upper = 0
        else:
            bottom = i - 1
            upper = i + 1
        lcl_pat = np.array([current[bottom], current[i], current[upper]])
        next[i] = rule[str(lcl_pat)]

    return next


d = rule8(90)
print(d)

full = np.zeros(shape=(200, 200), dtype=int)
np.random.seed(9)
full[0] = 1 * (np.random.random(size=200) > 0.9)
full[0][75] = 1
full[0][175] = 1
for i in range(1, len(full)):
    full[i] = next(full[i - 1], d)
plt.imshow(full, cmap='Greys')
plt.show()