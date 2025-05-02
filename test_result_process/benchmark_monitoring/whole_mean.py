'''
For each test scenario (e.g., bare-metal, docker, k3s...), multiple tests were conducted.
Each test result includes mean, standard deviation, minimum, and maximum values.
This script aggregates the test results within the same scenario, calculating the mean values.
'''

import pandas as pd
import os


# 测试不同的metric
metrics = ['CPU', 'RAM']
#test_scenarios = ['kvm-bare-metal', 'kvm-docker', 'kvm-k3s', 'wcm-bare-metal', 'wcm-docker-rosbag', 'wcm-k3s-rosbag-26', 'wcm-k3s-rosbag-10', 'wcm-k3s-rosbag-17','k3s-rosbag-5modules']
test_scenarios = ['wcm-bare-metal','k3s-rosbag-5modules-firstrun','k3s-rosbag-5modules-rerun']

def whole_mean(csv_folder_path, output_folder_path, test_scenario, metric):
    scenario_data = []
    for filename in os.listdir(csv_folder_path):
        if metric in filename and test_scenario in filename:
            csv_file_path = os.path.join(csv_folder_path, filename)

            # 读取CSV文件
            df = pd.read_csv(csv_file_path)
            scenario_data.append(df)
            
    all_data_df = pd.concat(scenario_data, ignore_index=True)
    result_df = pd.DataFrame({
        'Mean': all_data_df['Mean'].mean(),
        'Std': all_data_df['Std'].mean(),
        'Min': all_data_df['Min'].mean(),
        'Max': all_data_df['Max'].mean(),
    }, index=[0])

    
    output_file_path = os.path.join(output_folder_path, f'{test_scenario}-{metric}.csv')
    result_df.to_csv(output_file_path, index=False)
    #print(f"Mean {metric} for {test_scenario} saved")

# 指定CSV文件夹路径
csv_folder_path = os.path.join(os.getcwd(), 'whole-results')
output_folder = 'whole-mean-results'
output_folder_path = os.path.join(os.getcwd(), output_folder)
os.makedirs(output_folder_path, exist_ok=True)



# 调用函数处理不同的metric
for metric in metrics:
    for test_scenario in test_scenarios:
        whole_mean(csv_folder_path, output_folder_path, test_scenario, metric)
print('whole_mean.py finished')

