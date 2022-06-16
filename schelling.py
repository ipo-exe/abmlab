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
import os
import pandas as pd
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from backend import get_seed, get_window_ids, drop_center_cell, status


def world_random(df_sim_params, df_agt_params):
    """
    Generate a randomly distributed world of agents
    :param df_sim_params: pandas dataframe simulation parameters
    :param df_agt_params: pandas dataframe agent parameters
    :return: 2d numpy array
    """
    df_agt_params = df_agt_params.copy()
    df_agt_params.sort_values(by='Id', inplace=True)
    # get grid size
    n_grid = int(df_sim_params[df_sim_params['Parameter'] == 'N_Grid']['Set'].values[0])
    # initiate the world grid
    grd_world = np.zeros(shape=(n_grid, n_grid), dtype='uint8')
    #
    # set random state
    np.random.seed(get_seed())
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
    return grd_world


def compute_next(grd, df_agt_params, vct_rows_ids, vct_cols_ids):
    """
    Compute the next step world of the SSM
    :param grd: 2d numpy array of agents
    :param df_agt_params: pandas dataframe agent parameters
    :param vct_rows_ids: 1d numpy array base window row vector
    :param vct_cols_ids: 1d numpy array base window cols vector
    :return: 2d numpy array
    """
    # get seeds
    np.random.seed(get_seed())
    seeds = np.random.randint(0, 255, size=np.shape(grd), dtype='uint8')
    # get window parameters
    n_rows = len(grd)
    n_cols = len(grd[0])
    # scanning loop
    for i in range(len(grd)):
        for j in range(len(grd[i])):
            # access local i
            lcl_agent_id = grd[i][j]
            # skip voids
            if lcl_agent_id == 0:
                pass
            else:
                # get agent parameter
                lcl_agent_spr = df_agt_params[df_agt_params['Id'] == lcl_agent_id]['SPr'].values[0]
                '''
                # get window dict coordinates
                dw = get_window_xy_deprec(lcl_i=i, lcl_j=j, size_i=len(grd), size_j=len(grd[i]))
                # coordinate object
                dct_c = {'0': {'i': dw['nw']['y'], 'j': dw['nw']['x']},
                         '1': {'i': dw['n']['y'], 'j': dw['n']['x']},
                         '2': {'i': dw['ne']['y'], 'j': dw['ne']['x']},
                         '3': {'i': dw['w']['y'], 'j': dw['w']['x']},
                         '4': {'i': dw['e']['y'], 'j': dw['e']['x']},
                         '5': {'i': dw['sw']['y'], 'j': dw['sw']['x']},
                         '6': {'i': dw['s']['y'], 'j': dw['s']['x']},
                         '7': {'i': dw['se']['y'], 'j': dw['se']['x']}}

                # define flat window array
                vct_window = np.array([grd[dw['nw']['y']][dw['nw']['x']],
                                       grd[dw['n']['y']][dw['n']['x']],
                                       grd[dw['ne']['y']][dw['ne']['x']],
                                       grd[dw['w']['y']][dw['w']['x']],
                                       grd[dw['e']['y']][dw['e']['x']],
                                       grd[dw['sw']['y']][dw['sw']['x']],
                                       grd[dw['s']['y']][dw['s']['x']],
                                       grd[dw['se']['y']][dw['se']['x']]])
                
                '''
                # get the window vector
                vct_window = grd[(i + vct_rows_ids) % n_rows, (j + vct_cols_ids) % n_cols]

                # apply rules
                b_nonvoid = 1 * (vct_window > 0)  # boolean vector of non-void cells
                n_nonvoid = np.sum(b_nonvoid)  # sum of non-void cells
                b_void = 1 * (vct_window == 0)  # boolean vector of voids cells
                n_void = np.sum(b_void)  # sum of void cells
                b_match = 1 * (vct_window == lcl_agent_id)  # boolean of matching cells
                n_match = np.sum(b_match)  # sum of matching cells

                # access matching score
                if n_nonvoid > 0:
                    lcl_match_score = n_match / n_nonvoid # ratio of matching cell to non-void cells (occupied)
                    ### lcl_void_score = n_void / len(vct_window)  # ratio of voids
                else: # no neightboors around, bad situation
                    lcl_match_score = 0

                if lcl_match_score >= lcl_agent_spr:
                    ### print('good place, stay')
                    pass
                else:
                    ### print('bad place, you should move')
                    if np.sum(b_void) > 0:
                        ### print('there is empty cells around, you can move!')
                        # random movement
                        np.random.seed(seeds[i][j])  # set random state
                        # random scores where cells are void
                        vct_scores = np.random.random(size=len(vct_window)) * b_void
                        # get aux dataframe
                        df_aux = pd.DataFrame({'Rows_ids': (i + vct_rows_ids) % n_rows,
                                               'Cols_ids':  (j + vct_cols_ids) % n_cols,
                                               'Score': vct_scores})
                        # get new position
                        df_aux.sort_values(by='Score', ascending=False, inplace=True)
                        #
                        # exchange values in grid
                        new_i = df_aux['Rows_ids'].values[0]
                        new_j = df_aux['Cols_ids'].values[0]
                        grd[new_i][new_j] = lcl_agent_id
                        grd[i][j] = 0 # void value
    return grd


def play(grd_start, df_sim_params, df_agt_params, trace=True):
    """

    :param grd_start: 2d numpy array
    :param df_sim_params: pandas dataframe of simulation parameters
    :param df_agt_params: pandas dataframe
    :param trace: boolean to tracebak all model evolution
    :return: simulation object
    """
    # simulation object
    dct_out = {'Start' : grd_start.copy()}
    # get simulation steps
    n_steps = int(df_sim_params[df_sim_params['Parameter'] == 'N_Steps']['Set'].values[0])
    # get window paramters
    n_rows = len(grd_start)
    n_cols = len(grd_start[0])
    vct_rows_ids, vct_cols_ids = get_window_ids(n_rows=n_rows, n_cols=n_cols, n_rsize=1, b_flat=True)
    vct_rows_ids, vct_cols_ids = drop_center_cell(vct_window_rows=vct_rows_ids, vct_window_cols=vct_cols_ids)
    # set extra variables
    if trace:
        n_grid = int(df_sim_params[df_sim_params['Parameter'] == 'N_Grid']['Set'].values[0])
        grd3_traced = np.zeros(shape=(n_steps, n_grid, n_grid), dtype='uint8')
    # main loop
    for i in range(n_steps):
        status('step {}'.format(i))
        if trace:
            grd3_traced[i] = grd_start.copy()
        # compute next
        grd_start = compute_next(grd=grd_start,
                                 df_agt_params=df_agt_params,
                                 vct_rows_ids=vct_rows_ids,
                                 vct_cols_ids=vct_cols_ids)
    # output
    dct_out['End'] = grd_start.copy()
    if trace:
        dct_out['Evolution'] = grd3_traced
    return dct_out