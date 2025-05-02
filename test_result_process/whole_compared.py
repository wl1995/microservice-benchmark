import pandas as pd
import os

def calculate_percentage(base_scenario, test_scenarios, csv_folder_path, output_folder_path, metrics):
    for metric in metrics:
        metric_data = []
        # 构建基准数据文件路径
        base_file_path = os.path.join(csv_folder_path, f'{base_scenario}-{metric}.csv')
        base_df = pd.read_csv(base_file_path)

        for test_scenario in test_scenarios:

            # 构建测试情况数据文件路径
            test_file_path = os.path.join(csv_folder_path, f'{test_scenario}-{metric}.csv')
            test_df = pd.read_csv(test_file_path)

            # 计算百分比差异
            percentage_difference = (test_df / base_df) * 100

            percentage_difference['test_scenario'] = test_scenario
            metric_data.append(percentage_difference)

        # 保存结果到新的CSV文件
        output_percentage_path = os.path.join(output_folder_path, f'{base_scenario}-{metric}.csv')
        metric_data_df = pd.concat(metric_data, ignore_index=True)
        metric_data_df = metric_data_df[['test_scenario'] + metric_data_df.columns[:-1].tolist()]
        metric_data_df.to_csv(output_percentage_path, index=False)

        print(f"Compared {metric} for base scenario: {base_scenario} saved")



# 指定CSV文件夹路径
csv_folder_path = os.path.join(os.getcwd(), 'whole-mean-results')
output_folder = 'whole-compared-results'
output_folder_path = os.path.join(os.getcwd(), output_folder)
os.makedirs(output_folder_path, exist_ok=True)

# 遍历不同的metric（CPU、RAM、GPU）
metrics = ['CPU', 'RAM', 'GPU']

# Not KVM
base_scenario = 'wcm-bare-metal'
test_scenarios = ['wcm-docker-rosbag', 'wcm-k3s-rosbag-10', 'wcm-k3s-rosbag-17', 'wcm-k3s-rosbag-26']
calculate_percentage(base_scenario, test_scenarios, csv_folder_path, output_folder_path, metrics)


# KVM
base_scenario = 'kvm-bare-metal'
test_scenarios = ['kvm-docker', 'kvm-k3s']
calculate_percentage(base_scenario, test_scenarios, csv_folder_path, output_folder_path, metrics)
