'''

Cookbook scripts source code

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
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from visuals import plot_sigle_frame
from backend import create_rundir, get_seed, status
from out import export_gif

def cgl_recipe():
    import conway
    # workplace
    wkpl = '/home/ipora/Documents/bin'
    dir_out = create_rundir(label='CGL', wkplc=wkpl)
    dir_frames = '{}/frames'.format(dir_out)
    os.mkdir(dir_frames)

    # parameters
    n_gens = 20
    n_grid = 60
    r_density = 0.15

    # random state
    n_seed = get_seed()
    np.random.seed(n_seed)

    # get initial state
    ###grd_ini = np.array(1 * (np.random.random(size=(n_grid, n_grid)) < r_density), dtype='int8')
    grd_ini = conway.gosper_gun(n_grid=n_grid)
    ##grd_ini = conway.infinte_pattern(n_grid=n_grid)

    # play CGL
    status('running Conway Game of Life')
    trace = True
    dct_sim = conway.play(grd_ini, n_gens, n_grid, trace=trace)
    if trace:
        grd_run = dct_sim['Evolution']
        # export
        plt.style.use('dark_background')
        for i in range(len(grd_run)):
            status('exporting plot {}'.format(i + 1))
            lcl_fname = 'CGL_{}'.format(str(i).zfill(4))
            plot_sigle_frame(grd=grd_run[i],
                             cmap='Greys_r',
                             folder=dir_frames,
                             fname=lcl_fname,
                             ttl='t = {}'.format(i),
                             show=False,
                             dark=True)
        status('exporting gif animation')
        export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')


def wolfram_recipe():
    import wolfram
    # workplace
    wkpl = '/home/ipora/Documents/bin'
    dir_out = create_rundir(label='WLF', wkplc=wkpl)
    dir_frames = '{}/frames'.format(dir_out)
    os.mkdir(dir_frames)

    # parameters
    n_gens = 250
    n_cells = 50
    n_rule = 30

    # initial conditions
    vct_start = np.zeros(n_cells, dtype='uint8')
    vct_start[int(n_cells / 2)] = 1

    # run
    status('running wolfram cellular automata')
    grd_run = wolfram.play(vct_start=vct_start, n_gens=n_gens, n_rule=n_rule)

    # plot
    for i in range(len(grd_run) - n_cells):
        status('exporting plot {}'.format(i + 1))
        lcl_fname = 'WLF_{}'.format(str(i).zfill(4))
        plot_sigle_frame(grd=grd_run[i : i + n_cells],
                         cmap='Greys_r',
                         ttl='rule {} | t = {}'.format(n_rule, i),
                         folder=dir_frames,
                         fname=lcl_fname,
                         show=False,
                         dark=True)
    status('exporting gif animation')
    export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')


def schelling_recipe():
    from matplotlib.colors import ListedColormap
    import schelling
    # workplace
    wkpl = '/home/ipora/Documents/bin'
    dir_out = create_rundir(label='SSM', wkplc=wkpl)
    dir_frames = '{}/frames'.format(dir_out)
    os.mkdir(dir_frames)

    # parameters
    # simulation parameters
    df_sim_params = pd.DataFrame({'Parameter': ['N_Grid', 'R_Voids', 'N_Steps'],
                                  'Set': [30, 0.5, 100],
                                  'Min': [10, 0.05, 10],
                                  'Max': [100, 0.95, 100]
                                  })
    # agent parameters
    df_agt_params = pd.DataFrame({'Id': [1, 2],
                                  'Name': ['A', 'B'],
                                  'SPr': [0.5, 0.5],
                                  'Freq': [1, 1],
                                  'Color': ['olive', 'darkgreen']
                                   })

    # initial conditions
    grd_start = schelling.world_random(df_sim_params=df_sim_params, df_agt_params=df_agt_params)

    # run
    status('running schelling`s segregation model')
    trace = True
    dct_sim = schelling.play(grd_start, df_sim_params=df_sim_params, df_agt_params=df_agt_params, trace=trace)

    if trace:
        grd_run = dct_sim['Evolution']
        # plot
        colors = list(df_agt_params['Color'].values)
        colors.insert(0, 'silver')
        cmap = ListedColormap(colors=colors)
        for i in range(len(grd_run)):
            status('exporting plot {}'.format(i + 1))
            lcl_fname = 'SSM_{}'.format(str(i).zfill(4))
            plot_sigle_frame(grd=grd_run[i],
                             cmap=cmap,
                             ttl='t = {}'.format(i),
                             folder=dir_frames,
                             fname=lcl_fname,
                             show=False,
                             dark=True)
        status('exporting gif animation')
        export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')


#cgl_recipe()
#wolfram_recipe()
schelling_recipe()
