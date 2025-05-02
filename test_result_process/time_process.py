'''
    For each test, extract CPU and RAM usage in whole process
'''
import pandas as pd
import os

metrics = ['CPU', 'RAM', 'GPU']
test_scenarios = ['kvm-bare-metal', 'kvm-docker', 'kvm-k3s', 'wcm-bare-metal', 'wcm-docker-rosbag', 'wcm-k3s-rosbag-26', 'wcm-k3s-rosbag-10', 'wcm-k3s-rosbag-17']


def time_process(csv_folder_path, output_folder_path, test_scenario, metric):
    shortest_time = float('inf')
    scenario_data = []
    for foldername in os.listdir(csv_folder_path):
        if test_scenario in foldername:
            stats_path = os.path.join(csv_folder_path, foldername, 'cpu_mem_analysis/total')
            filename = f'{metric}_sums.csv'
            # 构建CSV文件的完整路径
            csv_file_path = os.path.join(stats_path, filename)

            # 读取CSV文件
            df = pd.read_csv(csv_file_path)

            # Extract the desired columns
            data_column = df.iloc[:, 0]

            shortest_time = min(len(data_column), shortest_time)
            scenario_data.append(data_column)

    trimmed_data = [df[:shortest_time] for df in scenario_data]
    trimmed_data_df = pd.concat(trimmed_data, axis=1)

    # Calculate the mean along the rows (axis=1)
    mean_data = trimmed_data_df.mean(axis=1)
    mean_data_df = pd.DataFrame(mean_data, columns=['Mean'])

    output_file_path = os.path.join(output_folder_path, f'{test_scenario}-{metric}.csv')
    mean_data_df.to_csv(output_file_path, index=False)
    #print(f"Mean {metric} for {test_scenario} saved")


def merge_to_dat(time_folder_path, output_folder_path, test_scenario, metrics):
    scenario_data = []
    for metric in metrics:
        for filename in os.listdir(time_folder_path):
            if test_scenario in filename and metric in filename:
                # 构建CSV文件的完整路径
                csv_file_path = os.path.join(time_folder_path, filename)

                # 读取CSV文件
                df = pd.read_csv(csv_file_path)

                # Extract the desired columns
                data_column = df.iloc[:, 0]

                scenario_data.append(data_column)

    scenario_data_df = pd.concat(scenario_data, axis=1)
    scenario_data_df.columns = metrics

    # Add colomn 'second'
    second_column = range(1, len(scenario_data_df) + 1)
    scenario_data_df.insert(0, 'second', second_column)

    output_file_path = os.path.join(output_folder_path, f'{test_scenario}-merged.dat')
    scenario_data_df.to_csv(output_file_path, sep=' ', index=False)

    #output_file_path = os.path.join(output_folder_path, f'{test_scenario}-merged.csv')
    #scenario_data_df.to_csv(output_file_path, index=False)

    print(f"Merged usage for {test_scenario} saved")



# output path of time process
csv_folder_path = os.path.join(os.getcwd(), 'data')
time_folder = 'time-results'
time_folder_path = os.path.join(os.getcwd(), time_folder)
os.makedirs(time_folder_path, exist_ok=True)


# 调用函数处理不同的metric
for test_scenario in test_scenarios:
    for metric in metrics: 
        time_process(csv_folder_path, time_folder_path, test_scenario, metric)


# Combine CPU, RAM, GPU into one file
merged_folder = 'time-results/merged'
merged_folder_path = os.path.join(os.getcwd(), merged_folder)
os.makedirs(merged_folder_path, exist_ok=True)

for test_scenario in test_scenarios:
    merge_to_dat(time_folder_path, merged_folder_path, test_scenario, metrics)
