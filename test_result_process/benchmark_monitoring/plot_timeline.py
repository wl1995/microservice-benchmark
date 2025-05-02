import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy.interpolate import make_interp_spline
from colorama import Fore
from colorama import init
init(autoreset=True)

import pprint

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size" : 8
})

plt.rc('text.latex', preamble=r'\usepackage[helvet]{sfmath}')

palette = {
    "sensing"       : "#bda5c9", # pink
    "localization"  : "#96bcf3", # blue
    "perception"    : "#a6cba4", # green
    "planning"      : "#fcde83", # yellow
    "control"       : "#fac185", # orange
    "map"           : "#8da3b4", # blueish gray
    "system"        : "#cfcfcf", # gray
    "other"         : "#7bccd1", # turquoise
    "simulation"    : "#ffcdcd", # red
    "rviz"          : "#b691fc", # purple

    "bare-metal"    : "#c8ced4", # grey
    "docker"        : "#4c84f1", # blue
    "k3s"           : "#fdd56d"  # yellow
}

# Can specify the performance indicators, e.g., leave only RAM
columns = ['CPU', 'RAM']

curve_names = {"rviz" : "RViz", "other" : "Vehicle\nInterface"}

configs = ["bare-metal", "docker", "k3s"]

page_width = 6.10356 # inches

# Specify the data and results folder paths
data_folder = 'data'
results_folder = 'results'

# Create the results folder if it doesn't exist
os.makedirs(results_folder, exist_ok=True)

# can spe
selected_experiments = ["bare-metal-planning-2", "docker-planning-4"]

# Get list of experiments (assuming each experiment has its own folder under the data folder)
experiments = sorted([dir for dir in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, dir)) and os.path.exists(os.path.join(data_folder, dir, "cpu_mem_analysis")) and dir in selected_experiments])

# Create dictionaries to store timeline data
timeline_data = {}

# Iterate over the experiments
for experiment in experiments:
    print(f"{Fore.GREEN}Starting for {experiment}")

    if experiment not in timeline_data:
        timeline_data[experiment] = []

    # hardcode folders to enforce order
    modules = ["sensing", "localization", "perception", "planning", "control", "map", "simulation", "system", "rviz", "other"]
    # enforce "other" being processed first
    modules.reverse()
    for i, module in enumerate(modules):
        cpu_path = os.path.join(data_folder, experiment, 'cpu_mem_analysis', module, 'CPU_sums.csv')
        mem_path = os.path.join(data_folder, experiment, 'cpu_mem_analysis', module, 'RAM_sums.csv')

        df_cpu = pd.read_csv(cpu_path, header=None)
        df_mem = pd.read_csv(mem_path, header=None)

        df_cpu.columns = ['CPU']
        df_mem.columns = ['RAM']

        df_duration = pd.read_csv(os.path.join(data_folder, experiment, 'duration.txt'))
        seconds_duration = df_duration["seconds"].iloc[0]
        timestamps_to_seconds_factor = df_duration["timestamps"].iloc[0] / seconds_duration

        cpu_index_list = df_cpu[df_cpu['CPU'].gt(0.0)].index
        mem_index_list = df_mem[df_mem['RAM'].gt(0.0)].index
        if len(cpu_index_list) == 0 and len(mem_index_list) == 0:
            continue
        elif len(cpu_index_list) == 0 or len(mem_index_list) == 0:
            raise ValueError(f'CPU or Memory usage is 0 but not both for "{module}"')

        cpu_first_timestamp = cpu_index_list[0]
        mem_first_timestamp = mem_index_list[0]
        first_timestamp = min(cpu_first_timestamp, mem_first_timestamp)
        # assume "other" always starts first
        if i == 0:
            global_first_timestamp = first_timestamp
        else:
            # check the assumption
            if first_timestamp < global_first_timestamp:
                component = ""
                if cpu_first_timestamp < global_first_timestamp:
                    component = "CPU"
                if mem_first_timestamp < global_first_timestamp:
                    if component != "":
                        component += " and RAM"
                    else:
                        component = "RAM"
                print(f'{Fore.RED}"{module}" started {component} {global_first_timestamp - first_timestamp} timestamps earlier than "other"')
                first_timestamp = global_first_timestamp

        last_timestamp = max(cpu_index_list[-1], mem_index_list[-1])

        df_cpu['Timestamp'] = df_cpu.index - global_first_timestamp
        df_mem['Timestamp'] = df_mem.index - global_first_timestamp

        df = pd.merge(df_cpu, df_mem, on='Timestamp')
        df = df[df.index >= first_timestamp]
        df = df[df.index <= last_timestamp]
        df['Timestamp'] /= timestamps_to_seconds_factor

        df['Experiment'] = experiment
        df['Module'] = module
        df['Duration'] = (last_timestamp - first_timestamp) / timestamps_to_seconds_factor
        timeline_data[experiment].append(df)

    # enforce "total" or "vehicle interface" being plotted last
    timeline_data[experiment].reverse()

subplots_per_row = 2
fig, ax = plt.subplots(ncols=len(experiments), nrows=(len(experiments) // subplots_per_row), layout='constrained')
fig.set_figwidth(page_width)
fig.set_figheight(page_width / 2)

names = ["Bare-metal", "Docker"]

for column in columns:
    for i, experiment in enumerate(timeline_data.keys()):
        ax[i].get_yaxis().get_major_formatter().set_useOffset(False)
        for experiment_df in timeline_data[experiment]:
            module = experiment_df['Module'].iloc[0]
            label = curve_names[module] if module in curve_names else module.capitalize()

            x = experiment_df['Timestamp'].values
            y = experiment_df[column].values
            spline = make_interp_spline(x, y)
            duration = np.floor(experiment_df['Duration'].iloc[0]).astype(int)
            x_interp = np.linspace(x.min(), x.max(), duration)
            y_interp = spline(x_interp)
            ax[i].plot(x_interp, y_interp, linewidth=1, label=label, color=palette[module])
        ax[i].set_xlabel('Seconds')
        ax[i].set_ylabel(f"{column} utilization with {names[i]} in \%")
        # set same bound for all subplots for better visual comparison
        ax[i].set_ybound(upper=8.5)
        ax[i].set_xbound(upper=165)
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].spines['bottom'].set_visible(False)
        ax[i].spines['left'].set_visible(False)

        ax[i].set_axisbelow(True)
        ax[i].yaxis.grid(True, color='#d4d4d4')
        ax[i].xaxis.grid(True, color='#d4d4d4')
        ax[i].tick_params(left=False, bottom=False)
        if i == 0:
            ax[i].legend()
    plt.xticks()        
    plt.savefig(os.path.join(results_folder, f'{column}_time.pdf'))
    plt.close(fig)