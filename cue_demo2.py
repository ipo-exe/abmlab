import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import backend


def play(vct_agents, vct_spaces):
    print()

# todo import from file
# >>> simulation parameters dataframe (import from csv file)
df_sim_params = pd.DataFrame({'Parameter': ['N_Agents',
                                            'N_Spaces',
                                            'N_Char',
                                            'R_Delta',
                                            'N_Rmax',
                                            'R_Agents',
                                            'R_Spaces',
                                            'N_Steps',],
                              'Set': [1, 15, 20, 1.0, 3, 0.1, 0.1, 45],
                              'Min': [10, 10, 100, 0.05, 3, 0.01, 0.001, 10],
                              'Max': [99, 99, 10000, 0.5, 9, 0.9, 0.1, 1000]
                              })
print(df_sim_params.to_string())

# >>> retrieve model parameters from dataframe to local variables:
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


# todo set dtype better (consider simulation parameters)
s_dtype = 'float32'

# >>> set simulation initial conditions:
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
    vct_agents_chars = 1 * np.ones(shape=n_agents, dtype=s_dtype)
    vct_agents_i = 9 * np.ones(shape=n_agents, dtype='uint16') #np.random.randint(low=0, high=n_spaces, size=n_agents, dtype='uint16')
    vct_spaces_chars = 19 * np.ones(shape=n_spaces, dtype=s_dtype)

# deploy simulation dataframes
df_agents = pd.DataFrame({'Agent_char': vct_agents_chars, 'Agent_i': vct_agents_i})
print(df_agents.to_string())
df_spaces = pd.DataFrame({'Space_char': vct_spaces_chars, 'Space_i': np.arange(0, n_spaces)})
print(df_spaces.to_string())

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

b_trace = True
if b_trace:
    grd_traced_agents_i = np.zeros(shape=(n_steps, n_agents), dtype=s_dtype)
    grd_traced_agents_chars = np.zeros(shape=(n_steps, n_agents), dtype=s_dtype)
    grd_traced_spaces_chars = np.zeros(shape=(n_steps, n_spaces), dtype=s_dtype)

# main simulation loop
for t in range(n_steps):
    #print('step {}'.format(t))
    # agents movements
    for a in range(n_agents):
        # get agent variables
        n_crt_agent_char = df_agents['Agent_char'].values[a]
        n_crt_agent_i = df_agents['Agent_i'].values[a]
        #print('Agent {} -- Current Char: {} -- Current Position: {}'.format(a, n_crt_agent_char, n_crt_agent_i))

        # get window dataframe
        df_window['Space_i'] = (n_crt_agent_i + vct_rows_base_ids) % n_spaces
        df_window['Space_char'] = df_spaces['Space_char'].values[df_window['Space_i'].values]
        df_window['Discrepancy'] = np.abs(n_crt_agent_char - df_window['Space_char'].values)

        # compute selection Interac_score
        df_window['Interac_score'] = df_window['Discrepancy'].max() - df_window['Discrepancy'] + 1 # normalize
        df_window['Interac_score'] = df_window['Interac_score'].values * (df_window['Discrepancy'].values <= n_delta_sigma)

        # compute probabilistic weights
        if df_window['Interac_score'].sum() == 0:
            df_window['Interac_prob'] = 1 / len(df_window)  # uniform distribution when all scores == 0
        else:
            df_window['Interac_prob'] = df_window['Interac_score'] / df_window['Interac_score'].sum()
        #df_window.sort_values(by='Interac_prob', ascending=False, inplace=True)
        #df_window.reset_index(drop=True, inplace=True)

        #print('Agent Window:')
        #print(df_window.to_string())

        # move agent
        np.random.seed(grd_seeds[t, a]) # restart random state
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

print(df_agents.to_string())
print(df_spaces.to_string())


# plot stuff



s_cmap = 'viridis' # 'tab20c'

grd_traced_spaces_chars_t = grd_traced_spaces_chars.transpose()
grd_traced_agents_i_t = grd_traced_agents_i.transpose()
grd_traced_agents_chars_t = grd_traced_agents_chars.transpose()

for t in range(n_steps - 1):
    print('plot {}'.format(t))
    if t < n_spaces:
        grd_lcl_spaces = grd_traced_spaces_chars_t[:, : t + 1]
        vct_lcl_agents_i = grd_traced_agents_i_t[a][: t + 1]
        vct_lcl_agents_chars = grd_traced_agents_chars_t[a][:t + 1]
        vct_lcl_ticks = np.arange(0, t + 1, 2)
        vct_lcl_labels = vct_lcl_ticks
    else:
        grd_lcl_spaces = grd_traced_spaces_chars_t[:, t - n_spaces: t + 1]
        vct_lcl_agents_i = grd_traced_agents_i_t[a][t - n_spaces:t + 1]
        vct_lcl_agents_chars = grd_traced_agents_chars_t[a][t - n_spaces:t + 1]
        vct_lcl_ticks = np.arange(0, n_spaces + 1, 2)
        vct_lcl_labels = vct_lcl_ticks + (t - n_spaces)
    #if t < n_spaces:
    #    grd_lcl[:, t:] = grd_traced_spaces_chars_t[:, t:]
    fig = plt.figure(figsize=(5, 5))  # Width, Height
    plt.suptitle('step = {}'.format(t))
    im = plt.imshow(grd_lcl_spaces, cmap=s_cmap, vmin=0, vmax=n_char)
    plt.colorbar(im, shrink=0.4)
    plt.xticks(ticks=vct_lcl_ticks, labels=vct_lcl_labels)
    '''
    for a in range(len(grd_traced_agents_i_t)):
        plt.plot(vct_lcl_agents_i, 'tab:grey', zorder=1)
    '''
    for a in range(len(grd_traced_agents_i_t)):
        plt.plot(vct_lcl_agents_i, 'tab:grey', zorder=1)

    for a in range(len(grd_traced_agents_i_t)):
        plt.scatter(np.arange(len(vct_lcl_agents_i)),
                    vct_lcl_agents_i,
                    c=vct_lcl_agents_chars,
                    edgecolors='white',
                    marker='o',
                    cmap=s_cmap,
                    vmin=0,
                    vmax=n_char,
                    zorder=2)


    #plt.xlim(t, t + n_spaces + 5)
    plt.ylabel('position')
    plt.xlabel('time step')
    #plt.show()
    plt.savefig('/home/ipora/Documents/bin/frame_{}'.format(str(t).zfill(4)), dpi=300)
    plt.close(fig)
    plt.clf()
    '''
    plt.hist(x=grd_traced_spaces_chars[0], bins=10)
    plt.xlim(0, n_char)
    plt.show()
    plt.hist(x=grd_traced_spaces_chars[n_steps-1], bins=10)
    plt.xlim(0, n_char)
    plt.show()
    
    '''