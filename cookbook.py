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
    n_gens = 50
    n_grid = 50
    r_density = 0.15

    # random state
    n_seed = get_seed()
    np.random.seed(n_seed)

    # get initial state
    ###grd_ini = np.array(1 * (np.random.random(size=(n_grid, n_grid)) < r_density), dtype='int8')
    grd_ini = conway.gosper_gun(n_grid=n_grid)
    #grd_ini = conway.infinte_pattern(n_grid=n_grid)

    # play CGL
    status('running Conway Game of Life')
    trace = True
    dct_sim = conway.play(grd_ini, n_gens, trace=trace)
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
    dir_out = create_rundir(label='WCA', wkplc=wkpl)
    dir_frames = '{}/frames'.format(dir_out)
    os.mkdir(dir_frames)

    # parameters
    n_gens = 250
    n_cells = 50
    n_rule = 90

    # initial conditions
    vct_start = np.zeros(n_cells, dtype='uint8')
    vct_start[int(n_cells / 2)] = 1

    # run
    status('running wolfram cellular automata')
    grd_run = wolfram.play(vct_start=vct_start, n_gens=n_gens, n_rule=n_rule)

    # plot
    for i in range(len(grd_run) - n_cells):
        status('exporting plot {}'.format(i + 1))
        lcl_fname = 'WCA_{}'.format(str(i).zfill(4))
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
    df_agt_params = pd.DataFrame({'Id': [1, 2, 3],
                                  'Name': ['A', 'B', 'C'],
                                  'SPr': [0.5, 0.5, 0.5],
                                  'Freq': [10, 10, 10],
                                  'Color': ['olive', 'darkgreen', 'tab:blue']
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


def cue_1d_recipe():
    import cue1d
    from visuals import plot_cue_1d_pannel
    # workplace
    wkpl = '/home/ipora/Documents/bin'
    dir_out = create_rundir(label='CUE1D', wkplc=wkpl)
    dir_frames = '{}/frames'.format(dir_out)
    os.mkdir(dir_frames)
    # todo import data from csv file
    # >>> simulation parameters dataframe (import from csv file)
    df_sim_params = pd.DataFrame({'Parameter': ['N_Agents',
                                                'N_Spaces',
                                                'N_Char',
                                                'R_Delta',
                                                'N_Rmax',
                                                'R_Agents',
                                                'R_Spaces',
                                                'N_Steps', ],
                                  'Set': [2, 40, 20, 1.0, 6, 0.01, 1.5, 200],
                                  'Min': [10, 10, 100, 0.05, 3, 0.01, 0.001, 10],
                                  'Max': [99, 99, 10000, 0.5, 9, 0.9, 0.1, 1000]
                                  })
    print(df_sim_params.to_string())

    # >>> retrieve model parameters from dataframe to local variables:
    status('retrieving simulation parameters')
    # number of agents:
    n_agents = int(df_sim_params[df_sim_params['Parameter'] == 'N_Agents']['Set'].values[0])

    # number of public spaces:
    n_spaces = int(df_sim_params[df_sim_params['Parameter'] == 'N_Spaces']['Set'].values[0])

    # number of unique characteristics:
    n_char = int(df_sim_params[df_sim_params['Parameter'] == 'N_Char']['Set'].values[0])

    # characteristic threshold for interaction:
    n_delta_sigma = int(n_char * df_sim_params[df_sim_params['Parameter'] == 'R_Delta']['Set'].values[0])
    print(n_delta_sigma)

    # distance threshold for interaction:
    n_rmax = int(df_sim_params[df_sim_params['Parameter'] == 'N_Rmax']['Set'].values[0])

    # number of time steps:
    n_steps = int(df_sim_params[df_sim_params['Parameter'] == 'N_Steps']['Set'].values[0])

    # extra paramters: (???)
    r_agents = df_sim_params[df_sim_params['Parameter'] == 'R_Agents']['Set'].values[0]
    r_spaces = df_sim_params[df_sim_params['Parameter'] == 'R_Spaces']['Set'].values[0]

    s_dtype = 'float32'
    # >>> set simulation initial conditions:
    status('getting simulation initial conditions')
    b_random = False
    if b_random:
        from backend import get_seed
        # set random state:
        np.random.seed(get_seed())
        # set uniform random distribution
        vct_agents_chars = np.round(n_char * np.random.random(size=n_agents), 0)
        vct_agents_i = np.random.randint(low=0, high=n_spaces, size=n_agents, dtype='uint16')
        vct_spaces_chars = np.round(n_char * np.random.random(size=n_spaces), 0)
    else:
        print('import from file')  # todo import from file
        vct_agents_chars = np.ones(shape=n_agents, dtype=s_dtype)
        vct_agents_chars[0] = 19
        vct_agents_chars[1] = 1
        vct_agents_i = np.ones(shape=n_agents, dtype='uint16')  # np.random.randint(low=0, high=n_spaces, size=n_agents, dtype='uint16')
        vct_agents_i[0] = 21
        vct_agents_i[1] = 19
        vct_spaces_chars = 10 * np.ones(shape=n_spaces, dtype=s_dtype)

    # deploy simulation dataframes
    df_agents = pd.DataFrame({'Agent_char': vct_agents_chars, 'Agent_i': vct_agents_i})
    print(df_agents.to_string())
    df_spaces = pd.DataFrame({'Space_char': vct_spaces_chars, 'Space_i': np.arange(0, n_spaces)})
    print(df_spaces.to_string())

    status('running cue 1d model')
    b_trace = True
    dct_out = cue1d.play(df_agents=df_agents,
                           df_spaces=df_spaces,
                           n_steps=n_steps,
                           r_agents=r_agents,
                           r_spaces=r_spaces,
                           n_rmax=n_rmax,
                           n_delta_sigma=n_delta_sigma,
                           b_trace=b_trace)

    if b_trace:
        # plot stuff
        status('plotting outputs')
        s_cmap = 'viridis'  # 'tab20c'

        grd_traced_spaces_chars_t = dct_out['Simulation']['Spaces_chars'].transpose()
        grd_traced_agents_i_t = dct_out['Simulation']['Agents_i'].transpose()
        grd_traced_agents_chars_t = dct_out['Simulation']['Agents_chars'].transpose()

        for t in range(n_steps - 1):
            #print('plot {}'.format(t))
            plot_cue_1d_pannel(step=t,
                               n_char=n_char,
                               n_spaces=n_spaces,
                               n_agents=n_agents,
                               spaces_chars_t=grd_traced_spaces_chars_t,
                               agents_chars_t=grd_traced_agents_chars_t,
                               agents_i_t=grd_traced_agents_i_t,
                               ttl='Step = {}'.format(t),
                               folder=dir_frames,
                               fname='frame_{}'.format(str(t).zfill(4)),
                               show=False,
                               dark=False)

        export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')

#cgl_recipe()
#wolfram_recipe()
#schelling_recipe()
cue_1d_recipe()
