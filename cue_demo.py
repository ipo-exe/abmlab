'''
Pilot 1dABM-CUE


'''

import numpy as np
import pandas as pd



def plot_run(grd_agents, grd_spaces, n_char=1000):
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    plt.style.use('dark_background')
    grd_agents_t = np.transpose(grd_agents)
    grd_spaces_t = np.transpose(grd_spaces)

    fig = plt.figure(figsize=(12, 6), )  # Width, Height
    gs = mpl.gridspec.GridSpec(2, 3, wspace=0.3, hspace=0.4, left=0.1, bottom=0.1, top=0.9, right=0.9)
    #
    ax = fig.add_subplot(gs[0, 0])
    plt.title('Agents')
    im = plt.imshow(grd_agents_t, cmap='tab20b', vmin=0, vmax=n_char)
    plt.xlabel('steps')
    plt.ylabel('position')
    plt.colorbar(im, shrink=0.4)
    #
    ax = fig.add_subplot(gs[1, 0])
    plt.title('Spaces')
    im = plt.imshow(grd_spaces_t, cmap='tab20b', vmin=0, vmax=n_char)
    plt.xlabel('steps')
    plt.ylabel('position')
    plt.colorbar(im, shrink=0.4)
    #
    ax = fig.add_subplot(gs[0, 1])
    plt.title('Agents')
    vct_steps = np.arange(0, len(grd_agents))
    for i in range(len(grd_agents_t)):
        plt.plot(vct_steps, grd_agents_t[i], c='tab:grey')
    plt.ylim(0, n_char)
    plt.xlim(0, len(grd_agents) - 1)
    plt.xlabel('steps')
    plt.ylabel('char')
    #
    ax = fig.add_subplot(gs[1, 1])
    plt.title('Spaces')
    vct_steps = np.arange(0, len(grd_spaces))
    for i in range(len(grd_spaces_t)):
        plt.plot(vct_steps, grd_spaces_t[i], c='tab:grey')
    plt.ylim(0, n_char)
    plt.xlim(0, len(grd_spaces) - 1)
    plt.xlabel('steps')
    plt.ylabel('char')
    #
    ax = fig.add_subplot(gs[0, 2])
    plt.title('Agents vs. Space - start')
    plt.scatter(grd_agents[0], grd_spaces[0], c='tab:grey', marker='.')
    plt.ylim(0, n_char)
    plt.xlim(0, n_char)
    plt.xlabel('agent char')
    plt.ylabel('space char')
    #
    ax = fig.add_subplot(gs[1, 2])
    plt.title('Agents vs. Space - end')
    plt.scatter(grd_agents[len(grd_agents) - 1], grd_spaces[len(grd_spaces) - 1], c='tab:grey', marker='.')
    plt.ylim(0, n_char)
    plt.xlim(0, n_char)
    plt.xlabel('agent char')
    plt.ylabel('space char')
    plt.show()


def compute_next_rand(vct_agents, vct_spaces, n_char=1000):
    vct_aux1 = np.random.randint(0, n_char, size=len(vct_agents))
    vct_aux2 = np.random.randint(0, n_char, size=len(vct_spaces))
    return vct_aux1, vct_aux2


def compute_next(vct_agents, vct_spaces, n_delta_sigma=10, n_rmax=3, r_agents=0.1, r_spaces=0.1):
    vct_next_agents = vct_agents.copy()
    vct_next_spaces = vct_spaces.copy()
    for i in range(len(vct_agents)):
        for j in range(len(vct_spaces)):
            # apply interaction criteria:
            b_distance = (np.abs(i - j) <= n_rmax)
            b_delta = (np.abs(int(vct_agents[i]) - int(vct_spaces[j])) <= n_delta_sigma)
            if b_distance and b_delta:
                # apply interaction to next gen (substitute last interaction)
                vct_next_agents[i] = (vct_agents[i] + (r_agents * vct_spaces[j])) / (1 + r_agents)
                vct_next_spaces[j] = (vct_spaces[j] + (r_spaces * vct_agents[i])) / (1 + r_spaces)
    #n_char = 100
    #vct_aux1 = np.random.randint(0, n_char, size=len(vct_agents), dtype='uint32')
    #vct_aux2 = np.random.randint(0, n_char, size=len(vct_spaces), dtype='uint32')
    return vct_next_agents, vct_next_spaces


def play(vct_agents, vct_spaces, df_sim_params, trace=True):
    # simulation object
    dct_out = {'Agents_Start': vct_agents.copy(),
               'Spaces_Start': vct_spaces.copy()}

    # >>> retrieve model parameters from dataframe to local variables:
    # number of agents:
    n_agents = int(df_sim_params[df_sim_params['Parameter'] == 'N_Agents']['Set'].values[0])
    # number of public spaces:
    n_spaces = int(df_sim_params[df_sim_params['Parameter'] == 'N_Spaces']['Set'].values[0])
    # number of unique characteristics:
    n_char = int(df_sim_params[df_sim_params['Parameter'] == 'N_Char']['Set'].values[0])
    # characteristic threshold for interaction:
    n_delta_sigma = int(n_char * df_sim_params[df_sim_params['Parameter'] == 'R_Delta']['Set'].values[0])
    # distance threshold for interaction:
    n_rmax = int(df_sim_params[df_sim_params['Parameter'] == 'N_Rmax']['Set'].values[0])
    # number of time steps:
    n_steps = int(df_sim_params[df_sim_params['Parameter'] == 'N_Steps']['Set'].values[0])
    # extra paramters: (???)
    r_agents = df_sim_params[df_sim_params['Parameter'] == 'R_Agents']['Set'].values[0]
    r_spaces = df_sim_params[df_sim_params['Parameter'] == 'R_Spaces']['Set'].values[0]

    if trace:
        # >>> declare simulation grids:
        grd_agents = np.zeros(shape=(n_steps, n_agents), dtype='uint16')
        grd_spaces = np.zeros(shape=(n_steps, n_spaces), dtype='uint16')
        # append start
        grd_agents[0] = vct_agents
        grd_spaces[0] = vct_spaces

    # simulation loop:
    for t in range(1, n_steps):
        print('step {}'.format(t))
        #vct_agents, vct_spaces = compute_next_rand(vct_agents=vct_agents, vct_spaces=vct_spaces, n_char=n_char)
        vct_agents, vct_spaces = compute_next(vct_agents=vct_agents,
                                              vct_spaces=vct_spaces,
                                              n_delta_sigma=n_delta_sigma,
                                              n_rmax=n_rmax,
                                              r_agents=r_agents,
                                              r_spaces=r_spaces)
        if trace:
            grd_agents[t] = vct_agents
            grd_spaces[t] = vct_spaces
    # output stuff
    if trace:
        dct_out['Sim_Agents'] = grd_agents.copy()
        dct_out['Sim_Spaces'] = grd_spaces.copy()
    dct_out['Agents_End'] = vct_agents.copy()
    dct_out['Spaces_End'] = vct_spaces.copy()
    return dct_out


# >>> simulation parameters dataframe (import from csv file)
df_sim_params = pd.DataFrame({'Parameter': ['N_Agents',
                                            'N_Spaces',
                                            'N_Char',
                                            'R_Delta',
                                            'N_Rmax',
                                            'R_Agents',
                                            'R_Spaces',
                                            'N_Steps',],
                              'Set': [50, 50, 100, 1.0, 2, 0.0, 0.5 , 50],
                              'Min': [10, 10, 100, 0.05, 3, 0.01, 0.001, 10],
                              'Max': [99, 99, 10000, 0.5, 9, 0.9, 0.1, 1000]
                              })
print(df_sim_params.to_string())

# number of agents:
n_agents = int(df_sim_params[df_sim_params['Parameter'] == 'N_Agents']['Set'].values[0])

# number of public spaces:
n_spaces = int(df_sim_params[df_sim_params['Parameter'] == 'N_Spaces']['Set'].values[0])

# number of unique characteristics:
n_char = int(df_sim_params[df_sim_params['Parameter'] == 'N_Char']['Set'].values[0])

# >>> set initial conditions:
b_random = True
if b_random:
    from backend import get_seed
    # set random state:
    np.random.seed(get_seed())
    # set uniform random distribution
    vct_agents = np.random.randint(low=0, high=n_char, size=n_agents, dtype='uint16')
    vct_agents = 60 * np.ones(shape=n_agents, dtype='uint16')
    vct_spaces = np.random.randint(low=0, high=n_char, size=n_spaces, dtype='uint16')
    #vct_spaces = 15 * np.ones(shape=n_agents, dtype='uint16')
else:
    print('import from file')

dct_out = play(vct_agents, vct_spaces, df_sim_params, True)
plot_run(grd_agents=dct_out['Sim_Agents'], grd_spaces=dct_out['Sim_Spaces'], n_char=n_char)



