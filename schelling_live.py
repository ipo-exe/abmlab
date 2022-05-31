'''

Schelling's Model of Segregation live mode source code

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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import schelling
from backend import get_seed


def beat(i):
    global grd_start
    global df_agt_params
    global cmap
    grd_start = schelling.compute_next(grd_start, df_agt_params)
    ax1.clear()
    plt.imshow(grd_start, cmap=cmap)
    plt.axis('off')

# parameters
# simulation parameters
df_sim_params = pd.DataFrame({'Parameter': ['N_Grid', 'R_Voids', 'N_Steps'],
                              'Set': [60, 0.5, 100],
                              'Min': [10, 0.05, 10],
                              'Max': [100, 0.95, 100]
                              })
# agent parameters
df_agt_params = pd.DataFrame({'Id': [1, 2],
                              'Name': ['A', 'B'],
                              'SPr': [0.8, 0.6],
                              'Freq': [4, 5],
                              'Color': ['olive', 'darkgreen']
                               })

# initial conditions
grd_start = schelling.world_random(df_sim_params=df_sim_params, df_agt_params=df_agt_params)


# animate
colors = list(df_agt_params['Color'].values)
colors.insert(0, 'silver')
cmap = ListedColormap(colors=colors)
plt.style.use('dark_background')
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(fig, func=beat, interval=10)
plt.show()