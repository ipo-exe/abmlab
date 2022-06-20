'''

CUE 1d routines source code

Copyright (C) 2022 Iporã Brito Possantti

References:


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
import backend


def play(df_agents, df_spaces, n_steps, n_rmax, n_delta_sigma, r_agents, r_spaces, b_trace=True):

    s_dtype = 'float32'
    n_agents = len(df_agents)
    n_spaces = len(df_spaces)

    # get scanning window parameters
    vct_window_rows, vct_window_cols = backend.get_window_ids(n_rows=n_spaces,
                                                              n_cols=n_spaces,
                                                              n_rsize=n_rmax,
                                                              b_flat=False)
    # remove the origin from window
    lst_aux = list()
    for e in vct_window_cols[0]:
        if e == 0:
            pass
        else:
            lst_aux.append(e)
    # get window base ids
    vct_rows_base_ids = np.array(lst_aux, dtype='uint16')

    # deploy recyclable window dataframe
    n_window_size = len(vct_rows_base_ids)
    df_window = pd.DataFrame({'Space_char': np.zeros(n_window_size, dtype=s_dtype),
                              'Space_i': np.zeros(n_window_size, dtype='uint16'),
                              'Discrepancy': np.zeros(n_window_size, dtype=s_dtype),
                              'Interac_score': np.zeros(n_window_size, dtype=s_dtype),
                              'Interac_prob': np.zeros(n_window_size, dtype=s_dtype),
                              })

    # define random seeds prior to simulation loop
    np.random.seed(backend.get_seed())
    grd_seeds = np.random.randint(low=100, high=999, size=(n_steps, n_agents), dtype='uint16')

    # tracing variables
    if b_trace:
        grd_traced_agents_i = np.zeros(shape=(n_steps, n_agents), dtype=s_dtype)
        grd_traced_agents_chars = np.zeros(shape=(n_steps, n_agents), dtype=s_dtype)
        grd_traced_spaces_chars = np.zeros(shape=(n_steps, n_spaces), dtype=s_dtype)

    # main simulation loop
    for t in range(n_steps):
        backend.status('simulation step {}'.format(t))
        # agents movements
        for a in range(n_agents):
            # get agent variables
            n_crt_agent_char = df_agents['Agent_char'].values[a]
            n_crt_agent_i = df_agents['Agent_i'].values[a]

            # get window dataframe
            df_window['Space_i'] = (n_crt_agent_i + vct_rows_base_ids) % n_spaces
            df_window['Space_char'] = df_spaces['Space_char'].values[df_window['Space_i'].values]
            df_window['Discrepancy'] = np.abs(n_crt_agent_char - df_window['Space_char'].values)

            # compute selection Interac_score
            df_window['Interac_score'] = df_window['Discrepancy'].max() - df_window['Discrepancy'] + 1  # normalize
            df_window['Interac_score'] = df_window['Interac_score'].values * (
                        df_window['Discrepancy'].values <= n_delta_sigma)

            # compute probabilistic weights
            if df_window['Interac_score'].sum() == 0:
                df_window['Interac_prob'] = 1 / len(df_window)  # uniform distribution when all scores == 0
            else:
                df_window['Interac_prob'] = df_window['Interac_score'] / df_window['Interac_score'].sum()

            # print('Agent Window:')
            # print(df_window.to_string())

            # move agent
            np.random.seed(grd_seeds[t, a])  # restart random state
            # weighted random sampling
            n_next_index = np.random.choice(a=df_window.index, size=1, p=df_window['Interac_prob'].values)

            # update agent position
            df_agents['Agent_i'].values[a] = df_window['Space_i'].values[n_next_index]

            # apply interaction criteria
            if df_window['Interac_score'].values[n_next_index] > 0:
                # interact

                # get space parameters from window dataframe
                n_crt_space_char = df_window['Space_char'].values[n_next_index]
                n_crt_space_i = df_window['Space_i'].values[n_next_index]

                # compute means
                r_mean_agent = (n_crt_agent_char + (r_agents * n_crt_space_char)) / (1 + r_agents)
                r_mean_space = (n_crt_space_char + (r_spaces * n_crt_agent_char)) / (1 + r_spaces)

                # replace in simulation dataframes
                df_agents['Agent_char'].values[a] = r_mean_agent
                df_spaces['Space_char'].values[n_crt_space_i] = r_mean_space

            # trace
            if b_trace:
                grd_traced_spaces_chars[t] = df_spaces['Space_char'].values
                grd_traced_agents_chars[t] = df_agents['Agent_char'].values
                grd_traced_agents_i[t] = df_agents['Agent_i'].values

    dct_output = {'Agents_end': df_agents, 'Spaces_end': df_spaces}
    if b_trace:
        dct_output['Simulation'] = {'Spaces_chars': grd_traced_spaces_chars,
                                    'Agents_chars': grd_traced_agents_chars,
                                    'Agents_i': grd_traced_agents_i}
    return dct_output