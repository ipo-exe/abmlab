'''

Schelling's Model of Segregation source code

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

import pandas as pd
import numpy as np
import os
from conway import get_window
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from out import export_gif
from backend import create_rundir


def world_random(df_sim_params, df_agt_params, seed=66):
    print()
    df_agt_params = df_agt_params.copy()
    df_agt_params.sort_values(by='Id', inplace=True)
    # get grid size
    n_grid = int(df_sim_params[df_sim_params['Parameter'] == 'N_Grid']['Set'].values[0])
    # initiate the world grid
    grd_world = np.zeros(shape=(n_grid, n_grid), dtype='uint8')
    #
    # set random state
    np.random.seed(seed)
    # random grid
    grd_rnd = np.random.random(size=(n_grid, n_grid))
    vct_probs = df_agt_params['Freq'].values / df_agt_params['Freq'].sum()
    vct_probs_acc = vct_probs.copy()
    for i in range(1, len(vct_probs)):
        vct_probs_acc[i] = vct_probs_acc[i] + vct_probs_acc[i - 1]
    for i in range(len(vct_probs)):
        # get local mask
        if i == 0:
            grd_lcl_mask = 1 * (grd_rnd <= vct_probs_acc[i])
        else:
            grd_lcl_mask = 1 * (grd_rnd > vct_probs_acc[i - 1]) * (grd_rnd <= vct_probs_acc[i])
        # map agents in the world
        grd_world = grd_world + (df_agt_params['Id'].values[i] * grd_lcl_mask)
    # get random non-voids mask
    r_voids = df_sim_params[df_sim_params['Parameter'] == 'R_Voids']['Set'].values[0]
    grd_nonvoid_mask = 1 * (np.random.random(size=(n_grid, n_grid)) > r_voids)
    # apply voids
    grd_world = grd_world * grd_nonvoid_mask
    #
    #
    # plotting
    plt.style.use('dark_background')
    colors = list(df_agt_params['Color'].values)
    colors.insert(0, 'silver')
    cmap = ListedColormap(colors=colors)
    plt.imshow(grd_world, cmap=cmap)
    plt.axis('off')
    plt.show()
    return grd_world


def compute_next(grd, df_agt_params):
    from datetime import datetime
    seed = np.random.seed(int(str(datetime.now())[-6:]))
    seeds = np.random.randint(0, 255, size=np.shape(grd), dtype='uint8')
    # scanning loop
    for i in range(len(grd)):
        for j in range(len(grd[i])):
            lcl_id = grd[i][j]
            # skip voids
            if lcl_id == 0:
                pass
            else:
                # get agent parameter
                lcl_ba = df_agt_params[df_agt_params['Id'] == lcl_id]['Ba'].values[0]
                # get window dict coordinates
                dw = get_window(lcl_i=i, lcl_j=j, size_i=len(grd), size_j=len(grd[i]))

                # define indexed window map object
                dct_w = {'0': grd[dw['nw']['y']][dw['nw']['x']],
                         '1': grd[dw['n']['y']][dw['n']['x']],
                         '2': grd[dw['ne']['y']][dw['ne']['x']],
                         '3': grd[dw['w']['y']][dw['w']['x']],
                         '4': grd[dw['e']['y']][dw['e']['x']],
                         '5': grd[dw['sw']['y']][dw['sw']['x']],
                         '6': grd[dw['s']['y']][dw['s']['x']],
                         '7': grd[dw['se']['y']][dw['se']['x']]}

                # coordinate object
                dct_c = {'0': {'i': dw['nw']['y'], 'j': dw['nw']['x']},
                         '1': {'i': dw['n']['y'], 'j': dw['n']['x']},
                         '2': {'i': dw['ne']['y'], 'j':  dw['ne']['x']},
                         '3': {'i': dw['w']['y'], 'j': dw['w']['x']},
                         '4': {'i': dw['e']['y'], 'j': dw['e']['x']},
                         '5': {'i': dw['sw']['y'], 'j': dw['sw']['x']},
                         '6': {'i': dw['s']['y'], 'j': dw['s']['x']},
                         '7': {'i': dw['se']['y'], 'j': dw['se']['x']}}

                # define flat window array
                window = np.array([dct_w['0'],
                                   dct_w['1'],
                                   dct_w['2'],
                                   dct_w['3'],
                                   dct_w['4'],
                                   dct_w['5'],
                                   dct_w['6'],
                                   dct_w['7'] ])
                #
                #
                # apply rules
                b_nonvoid = 1 * (window > 0)
                n_nonvoid = np.sum(b_nonvoid)
                b_void = 1 * (window == 0)
                b_match = 1 * (window == lcl_id)
                #
                # access score
                if n_nonvoid > 0:
                    lcl_score = np.sum(b_match) / np.sum(b_nonvoid)
                else: # no neightboors around, bad situation
                    lcl_score = 0
                if lcl_score >= lcl_ba:
                    #print('good place, stay')
                    pass
                else:
                    #print('bad place')
                    if np.sum(b_void) > 0:
                        #print('you can move')
                        #
                        #
                        # random movement # todo preference-based scores
                        # set random state
                        seed = seeds[i][j]
                        np.random.seed(seed)
                        vct_random_scores = np.random.random(size=len(window)) * b_void
                        df_aux = pd.DataFrame({'Window_id': [0, 1, 2, 3, 4, 5, 6, 7],
                                               'Score': vct_random_scores})
                        df_aux.sort_values(by='Score', ascending=False, inplace=True)
                        n_new_position = df_aux['Window_id'].values[0]
                        #
                        #
                        #
                        # reset values in grid
                        new_i = dct_c[str(n_new_position)]['i']
                        new_j = dct_c[str(n_new_position)]['j']
                        grd[new_i][new_j] = lcl_id
                        grd[i][j] = 0
    return grd


def play(df_sim_params, df_agt_params, trace=True):
    from datetime import datetime
    wkpl = '/home/ipora/Documents/bin'
    dir_out = create_rundir(label='SSM', wkplc=wkpl)
    dir_frames = os.mkdir('{}/frames'.format(dir_out))
    dir_frames = '{}/frames'.format(dir_out)
    print(dir_frames)

    colors = list(df_agt_params['Color'].values)
    colors.insert(0, 'silver')
    cmap = ListedColormap(colors=colors)
    # set random state
    seed = np.random.seed(int(str(datetime.now())[-6:]))
    # get the world
    grd_world = world_random(df_sim_params=df_sim_params, df_agt_params=df_agt_params, seed=seed)
    dct_out = {'World_start': grd_world.copy()}
    #
    n_steps = int(df_sim_params[df_sim_params['Parameter'] == 'N_Steps']['Set'].values[0])
    if trace:
        n_grid = int(df_sim_params[df_sim_params['Parameter'] == 'N_Grid']['Set'].values[0])
        grd3_traced = np.zeros(shape=(n_steps, n_grid, n_grid), dtype='uint8')

    for i in range(n_steps):
        print('Step {}'.format(i))
        if trace:
            grd3_traced[i] = grd_world.copy()
        # compute next
        grd_world = compute_next(grd=grd_world, df_agt_params=df_agt_params)
        #
        # plot
        plt.style.use('dark_background')
        plt.imshow(grd_world, cmap=cmap)
        plt.axis('off')
        plt.title('Step = {}'.format(i))
        plt.savefig('{}/SSM_{}.png'.format(dir_frames, str(i).zfill(4)))
        plt.close()
    export_gif(dir_output=dir_out, dir_images=dir_frames, nm_gif='animation', kind='png', suf='')
    # output
    dct_out['World_end'] = grd_world.copy()
    if trace:
        dct_out['Evolution': grd3_traced]
    return grd_world


df_sim_params = pd.DataFrame({'Parameter': ['N_Grid', 'R_Voids', 'N_Steps'],
                              'Set': [30, 0.2, 300],
                              'Min': [10, 0.05, 10],
                              'Max': [100, 0.95, 100]
                              })

print(df_sim_params)
df_agt_params = pd.DataFrame({'Id' : [1, 2],
                              'Name': ['A', 'B'],
                              'Ba': [0.9, 0.9],
                              'Freq': [1, 1],
                              'Color': ['olive', 'darkgreen']
                              })


n_grid = df_sim_params[df_sim_params['Parameter'] == 'N_Grid']['Set'].values[0]
n_size = n_grid * n_grid
n_voids = int(n_size * df_sim_params[df_sim_params['Parameter'] == 'R_Voids']['Set'].values[0])
n_agents = n_size - n_voids

# compute the number of agents
df_agt_params['N'] = 0
for i in range(len(df_agt_params)):
    df_agt_params['N'].values[i] = n_agents * df_agt_params['Freq'].values[i] / df_agt_params['Freq'].sum()
print(df_agt_params.to_string())

play(df_sim_params=df_sim_params, df_agt_params=df_agt_params, trace=False)