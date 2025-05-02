import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import re
import pandas as pd
import pprint

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size" : 10
})

plt.rc('text.latex', preamble=r'\usepackage[helvet]{sfmath}')

palette = {
    "bare-metal"    : "#c8ced4", # grey
    "docker"        : "#4c84f1", # blue
    "k3s"           : "#fdd56d"  # yellow
}

total_gpu_mem = 12288 #MiB

max_watt = 350

page_width = 6.10356

configs = ["bare-metal", "docker", "k3s"]

pattern = r'\| *(\d+)%\s+\d+C\s+P\d+\s+(\d+)W / \d+W \|.*?(\d+)%'

pattern_lidar = r'.*lidar_centerpoint_node.*?(\d+)MiB\s*\|'
pattern_container = r'.*component_container_mt.*?(\d+)MiB\s*\|'

def parse_file(started, filename):
    """
    Parses the output of nvidia-smi.

    :param started: indicates whether the Autoware started based on previously read values
    :param filename: file that contains the nvidia-smi output 

    :return: (started, fan_usage, watt, gpu_util, mem_util)
    """
    with open(filename, "r") as f:
        input_text = f.read()

        matches = re.findall(pattern, input_text, re.MULTILINE)
        if not matches:
            if started:
                return False, 0, 0, 0, 0
            else:
                raise ValueError

        for match in matches:
            fan_usage = int(match[0])
            watt = int(match[1])
            gpu_util = int(match[2])

        mem_util = 0

        matches_lidar = re.findall(pattern_lidar, input_text, re.MULTILINE)
        matches_container = re.findall(pattern_container, input_text, re.MULTILINE)
        if len(matches_lidar) + len(matches_container) == 0:
            return False, 0, 0, 0, 0
        for match in matches_lidar + matches_container:
            mem_util += int(match)

    return True, fan_usage, watt, gpu_util, mem_util


data_folder = "data"
results_folder = "results"

experiments = [dir for dir in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, dir)) and "rosbag" in dir and "ignore" not in dir]

columns = {"GPU" : "gpu", "GPU memory" : "gpumem", "Power" : "gpupower", "Fan" : "gpufan"}

for experiment in experiments:
    if os.path.exists(os.path.join(results_folder, experiment, "gpu.csv")):
        continue
    df = pd.DataFrame(columns=columns.keys())
    monitoring_data = [dir for dir in os.listdir(os.path.join(data_folder, experiment)) if dir.startswith("monitoring_results_")]
    timestamp_data = [os.path.join(data_folder, experiment, monitoring_data[-1], f) for f in os.listdir(os.path.join(data_folder, experiment, monitoring_data[-1])) if f.startswith("gpu_memory_")]
    timestamp_data.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    started = False
    for timestamp in timestamp_data:
        status, fan_usage, watt, gpu_util, mem_util = parse_file(started, timestamp)
        if status and not started:
            started = True
        elif not status and started:
            break
        if status:
            df.loc[len(df)] = [gpu_util, mem_util / total_gpu_mem * 100, watt / max_watt * 100, fan_usage]
    os.makedirs(os.path.join(results_folder, experiment), exist_ok=True)
    df.to_csv(os.path.join(results_folder, experiment, "gpu.csv"), index=False)

data = {}

experiments = sorted([dir for dir in os.listdir(results_folder) if os.path.isdir(os.path.join(results_folder, dir)) and "rosbag" in dir and "ignore" not in dir])

for experiment in experiments:
    if "bare-metal" in experiment:
        config = "bare-metal"
    elif "docker" in experiment:
        config = "docker"
    elif "k3s" in experiment:
        config = "k3s"
    else:
        raise ValueError(f"Unknown config in {experiment}") 

    df = pd.read_csv(os.path.join(results_folder, experiment, "gpu.csv"), header=0)

    for column in df.columns:
        if column not in data:
            data[column] = {}  
        if config not in data[column]:
            data[column][config] = {"mean" : [], "var" : []}
        
        if column == "GPU memory":
            data[column][config]["mean"].append(df[column].mode()[0])
            data[column][config]["var"].append(0)
        else:
            data[column][config]["mean"].append(df[column].mean())
            data[column][config]["var"].append(df[column].var())

# pprint.pprint(data)

# calculate deviation of mean values across runs for each parameter and config
# print if above 5%
for metric, metric_data in data.items():
    for config, config_data in metric_data.items():
        std = np.std(config_data['mean'])
        mean = np.mean(config_data['mean'])
        std_p = round(std / mean * 100, 3)
        if std_p > 5.0:
            print(f'{metric} {config} has std = {std_p}% of mean')





