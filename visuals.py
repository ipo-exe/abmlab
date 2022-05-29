'''

Visuals routines source code

Copyright (C) 2022 Iporã Brito Possantti

References:
Schelling, Thomas C. (1971).
"Dynamic models of segregation". The Journal of Mathematical Sociology.
Informa UK Limited. 1 (2): 143–186.
doi:10.1080/0022250x.1971.9989794. ISSN 0022-250X.

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

import matplotlib.pyplot as plt


def plot_sigle_frame(grd,
                     cmap='Greys',
                     folder='C:/bin',
                     fname='frame',
                     suff='',
                     ttl='',
                     show=False,
                     dark=True,
                     dpi=300):
    if dark:
        plt.style.use('dark_background')
    fig = plt.figure(figsize=(4, 4))  # Width, Height
    plt.suptitle(ttl)
    plt.imshow(grd, cmap=cmap)
    plt.axis('off')
    if show:
        plt.show()
        plt.close(fig)
    else:
        # export file
        if suff == '':
            filepath = folder + '/' + fname + '.png'
        else:
            filepath = folder + '/' + fname + '_' + suff + '.png'
        plt.savefig(filepath, dpi=dpi)
        plt.close(fig)
        return filepath


