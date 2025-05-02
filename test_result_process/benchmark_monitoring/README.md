# Utilization of Hardware Resources by Autoware Components

## Collect Data

1. 
```bash
sudo bash monitor_processes.sh <experiment-name>
```
Note: experiment name must contain `rosbag` or `planning`

2. Launch experiment
3. Ctrl + C

## Process Data

4. 
```bash
python analyze_cpu_memory.py    # filter CPU and RAM processes
python analyze_gpu_memory.py    # create stats and plots for GPU data
```

5. To create stats and plots for CPU and RAM data, use [analyze_util.ipynb](./analyze_util.ipynb) and follow the instructions in the notebook.

Note: [plot_timeline.py](./plot_timeline.py) was used to plot the **CPU and RAM usage over time** for **2 selected experiments** as subplots of one figure. This was needed for the paper. It can be used for other experiments if the experiment names, the number of subplots, and the plot width are adjusted accordingly. The [analyze_gpu_memory.py](./analyze_gpu_memory.py) also plots the selected KPIs in one figure.