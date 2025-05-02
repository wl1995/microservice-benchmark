import os
import pandas as pd
import re
from colorama import Fore
from colorama import init
init(autoreset=True)

def keyword(module):
    """
    :param module: Autoware component or RViz
    :return: keyword used to filter processes of the module
    """
    if module == "rviz":
        return "rviz"
    else:
        return f"__ns:=/{module}"

# Define a function to parse a line considering quotes
def parse_line(line):
    match = re.search(r';?(\d*);([\d.]*);([\d.]*);(.*)', line)
    if match is None:
        return None
    return [match.group(2),  # %CPU
            match.group(3),  # %MEM
            match.group(4)]  # CMD

# Define a function to parse a filename and return a DataFrame
def parse_file(filename):
    # Extract the timestamp from the filename
    timestamp = filename.split('_')[-1].split('.')[0]

    # Read the file line by line and apply the parse function
    with open(filename, 'r') as file:
        content = file.readlines()

    parsed_content = [parse_line(line) for line in content[1:]]  # Skip header line
    parsed_content = [line for line in parsed_content if line is not None]  # Filter out any failed parses

    # Convert the parsed content to a dataframe
    data = pd.DataFrame(parsed_content, columns=['%CPU', '%MEM', 'CMD'])

    # Convert the %CPU and %MEM columns to appropriate data types
    data['%CPU'] = pd.to_numeric(data['%CPU'], errors='coerce')
    data['%MEM'] = pd.to_numeric(data['%MEM'], errors='coerce')

    # Rename %CPU and %MEM columns to include the timestamp
    data = data.rename(columns={'%CPU': '%CPU_' + timestamp, '%MEM': '%MEM_' + timestamp})

    return data

# Get a list of all runs
data_dir = "data"
modules = ["sensing", "localization", "perception", "planning", "control", "map", "system", "simulation", "rviz"]
runs = sorted([dir for dir in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, dir)) and "ignore" not in dir])
save_dir = "data"
processed_runs = 0

# exclude ros_trace, rosbag replay procees and bash scripts
excluded_processes = ["trace", "sqlite", "/bin/bash", "/bin/sh"]

for run in runs:
    cpu_mem_analysis_dir = os.path.join(save_dir, run, "cpu_mem_analysis")
    print(f"{Fore.GREEN}Starting for {run}")

    if not (os.path.exists(os.path.join(cpu_mem_analysis_dir, "cpu_data.csv")) and os.path.exists(os.path.join(cpu_mem_analysis_dir, "mem_data.csv"))):

        os.makedirs(cpu_mem_analysis_dir, exist_ok=True)

        # Specify the path to your csv directory
        run_dir = os.path.join(data_dir, run)

        csv_dirs = sorted([os.path.join(run_dir, d) for d in os.listdir(run_dir) if os.path.isdir(os.path.join(run_dir, d)) and d.startswith('monitoring_results_')])
        csv_dir = csv_dirs[-1]

        # Get a list of all csv files in the directory that start with "cpu_memory_", and sort them
        csv_files = sorted([os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.startswith('cpu_memory_') and f.endswith('.csv')])
        num_file = 0
        # Initialize a list to hold dataframes
        dfs_cpu = []
        dfs_mem = []

        # Process each file individually
        for file in csv_files:
            df = parse_file(file)
            df_cpu = df[['CMD'] + [col for col in df.columns if '%CPU' in col]]
            df_mem = df[['CMD'] + [col for col in df.columns if '%MEM' in col]]
            dfs_cpu.append(df_cpu)
            dfs_mem.append(df_mem)
            num_file += 1

        # Concatenate all dataframes along the row axis
        cpu_data_long = pd.concat(dfs_cpu, axis=0, sort=True)
        mem_data_long = pd.concat(dfs_mem, axis=0, sort=True)

        cpu_data = cpu_data_long.groupby("CMD").sum()
        mem_data = mem_data_long.groupby("CMD").sum()

        # Strip prefix and convert to integer for sorting
        cpu_data.reset_index(inplace=True)
        cpu_data.columns = [col.replace('%CPU_', '') for col in cpu_data.columns]

        mem_data.reset_index(inplace=True)
        mem_data.columns = [col.replace('%MEM_', '') for col in mem_data.columns]

        # Separate string and integer columns
        cpu_string_columns = cpu_data[['CMD']]
        cpu_integer_columns = cpu_data.drop(['CMD'], axis=1)

        mem_string_columns = mem_data[['CMD']]
        mem_integer_columns = mem_data.drop(['CMD'], axis=1)

        # Sort integer columns
        cpu_integer_columns = cpu_integer_columns.reindex(sorted(cpu_integer_columns.columns, key=int), axis=1)
        mem_integer_columns = mem_integer_columns.reindex(sorted(mem_integer_columns.columns, key=int), axis=1)

        # Concatenate string and integer columns
        cpu_data = pd.concat([cpu_string_columns, cpu_integer_columns], axis=1)
        mem_data = pd.concat([mem_string_columns, mem_integer_columns], axis=1)

        # Now, cpu_data and mem_data are your final tables for CPU and memory respectively
        # Saving the dataframes to csv files
        cpu_data.to_csv(os.path.join(cpu_mem_analysis_dir, "cpu_data.csv"), index=False)
        mem_data.to_csv(os.path.join(cpu_mem_analysis_dir, "ram_data.csv"), index=False)
    else:
        cpu_data = pd.read_csv(os.path.join(cpu_mem_analysis_dir, "cpu_data.csv"))
        mem_data = pd.read_csv(os.path.join(cpu_mem_analysis_dir, "mem_data.csv"))

    print(f"\tRetrieved cpu and mem data")

    # Remove trailing whitespaces and newlines from 'CMD' column
    cpu_data['CMD'] = cpu_data['CMD'].str.strip()
    cpu_data = cpu_data[~cpu_data['CMD'].str.contains('|'.join(excluded_processes), case=False)]

    mem_data['CMD'] = mem_data['CMD'].str.strip()
    mem_data = mem_data[~mem_data['CMD'].str.contains('|'.join(excluded_processes), case=False)]

    ### "container" = "total" + container-related processes
    if 'docker' in run:
        keywords = ["galactic", "autoware", "tier4", "dockerd", "container",  "ros2", "--ros-args"]
        os.makedirs(os.path.join(cpu_mem_analysis_dir, 'container'), exist_ok=True)
        cpu_data_filtered = cpu_data[cpu_data['CMD'].str.contains('|'.join(keywords), case=False)]
        mem_data_filtered = mem_data[mem_data['CMD'].str.contains('|'.join(keywords), case=False)]
        cpu_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "CPU_data_filtered.csv"), index=False)
        mem_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "RAM_data_filtered.csv"), index=False)
        cpu_sums = cpu_data_filtered.drop(columns=['CMD']).sum()
        mem_sums = mem_data_filtered.drop(columns=['CMD']).sum()
        cpu_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "CPU_sums.csv"), index=False, header=True)
        mem_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "RAM_sums.csv"), index=False, header=True)
    elif 'k3s' in run:
        keywords = ["galactic", "autoware", "tier4", "dockerd", "container", "k3s", "ros2", "--ros-args"] 
        os.makedirs(os.path.join(cpu_mem_analysis_dir, 'container'), exist_ok=True)
        cpu_data_filtered = cpu_data[cpu_data['CMD'].str.contains('|'.join(keywords), case=False)]
        mem_data_filtered = mem_data[mem_data['CMD'].str.contains('|'.join(keywords), case=False)]
        cpu_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "CPU_data_filtered.csv"), index=False)
        mem_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "RAM_data_filtered.csv"), index=False)
        cpu_sums = cpu_data_filtered.drop(columns=['CMD']).sum()
        mem_sums = mem_data_filtered.drop(columns=['CMD']).sum()
        cpu_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "CPU_sums.csv"), index=False, header=True)
        mem_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "container", "RAM_sums.csv"), index=False, header=True)

    keywords = ["galactic", "autoware", "tier4", "component_container", "ros2", "--ros-args"]
    
    ### "total" = all Autoware-related AND not container-related processes
    os.makedirs(os.path.join(cpu_mem_analysis_dir, 'total'), exist_ok=True)

    cpu_data_filtered = cpu_data[cpu_data['CMD'].str.contains('|'.join(keywords), case=False)]
    mem_data_filtered = mem_data[mem_data['CMD'].str.contains('|'.join(keywords), case=False)]

    # filter out docker keyword (can trap there because of commands like docker run autoware etc.)
    cpu_data_filtered = cpu_data_filtered[~cpu_data_filtered['CMD'].str.contains('|'.join(["docker"]), case=False)]
    mem_data_filtered = mem_data_filtered[~mem_data_filtered['CMD'].str.contains('|'.join(["docker"]), case=False)]

    cpu_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "total", "CPU_data_filtered.csv"), index=False)
    mem_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, "total", "RAM_data_filtered.csv"), index=False)

    # Replace NaN values with 0
    #cpu_data_filtered.fillna(0, inplace=True)
    #mem_data_filtered.fillna(0, inplace=True)

    # Calculate the sum of each column, ignoring 'CMD' and 'PID'
    cpu_sums = cpu_data_filtered.drop(columns=['CMD']).sum()
    mem_sums = mem_data_filtered.drop(columns=['CMD']).sum()

    cpu_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "total", "CPU_sums.csv"), index=False, header=True)
    mem_sums.to_csv(os.path.join(cpu_mem_analysis_dir, "total", "RAM_sums.csv"), index=False, header=True)

    ### "other" = processes from "total" that do not contain keywords of any module
    os.makedirs(os.path.join(cpu_mem_analysis_dir, 'other'), exist_ok=True)

    cpu_data_filtered = cpu_data_filtered[~cpu_data_filtered['CMD'].str.contains('|'.join([keyword(module) for module in modules]), case=False)]
    mem_data_filtered = mem_data_filtered[~mem_data_filtered['CMD'].str.contains('|'.join([keyword(module) for module in modules]), case=False)]

    cpu_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, 'other', "CPU_data_filtered.csv"), index=False)
    mem_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, 'other', "RAM_data_filtered.csv"), index=False)

    # Replace NaN values with 0
    #cpu_data_filtered.fillna(0, inplace=True)
    #mem_data_filtered.fillna(0, inplace=True)

    # Calculate the sum of each column, ignoring 'CMD' and 'PID'
    cpu_sums = cpu_data_filtered.drop(columns=['CMD']).sum()
    mem_sums = mem_data_filtered.drop(columns=['CMD']).sum()

    cpu_sums.to_csv(os.path.join(cpu_mem_analysis_dir, 'other', "CPU_sums.csv"), index=False, header=True)
    mem_sums.to_csv(os.path.join(cpu_mem_analysis_dir, 'other', "RAM_sums.csv"), index=False, header=True)

    ### for each module
    for module in modules:
        os.makedirs(os.path.join(cpu_mem_analysis_dir, module), exist_ok=True)
        cpu_data_filtered = cpu_data[cpu_data['CMD'].str.contains(keyword(module), case=False)]
        mem_data_filtered = mem_data[mem_data['CMD'].str.contains(keyword(module), case=False)]

        cpu_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, module, "CPU_data_filtered.csv"), index=False)
        mem_data_filtered.to_csv(os.path.join(cpu_mem_analysis_dir, module, "RAM_data_filtered.csv"), index=False)

        # Replace NaN values with 0
        #cpu_data_filtered.fillna(0, inplace=True)
        #mem_data_filtered.fillna(0, inplace=True)

        # Calculate the sum of each column, ignoring 'CMD' and 'PID'
        cpu_sums = cpu_data_filtered.drop(columns=['CMD']).sum()
        mem_sums = mem_data_filtered.drop(columns=['CMD']).sum()

        cpu_sums.to_csv(os.path.join(cpu_mem_analysis_dir, module, "CPU_sums.csv"), index=False, header=True)
        mem_sums.to_csv(os.path.join(cpu_mem_analysis_dir, module, "RAM_sums.csv"), index=False, header=True)

    processed_runs +=1

    print(f"\tFinished {run}, {processed_runs}/{len(runs)} runs")