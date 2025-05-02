'''
    For each test, extract CPU and RAM usage in whole process
    calculate the mean, standard deviation, minimum and maximum
'''
import pandas as pd
import os


# 测试不同的metric（CPU、RAM）
metrics = ['CPU', 'RAM', 'GPU']


def process_metric(csv_folder_path, output_folder_path, metric):
    for foldername in os.listdir(csv_folder_path):
        stats_path = os.path.join(csv_folder_path, foldername, 'cpu_mem_analysis/total')
        filename = f'{metric}_sums.csv'
        # 构建CSV文件的完整路径
        csv_file_path = os.path.join(stats_path, filename)

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # Extract the desired columns
        data_column = df.iloc[:, 0]

        mean_value = data_column.mean()
        std_deviation = data_column.std()
        min_value = data_column.min()
        max_value = data_column.max()

        result_df = pd.DataFrame({
            'Mean': [mean_value],
            'Std': [std_deviation],
            'Min': [min_value],
            'Max': [max_value]
        })

        output_file_path = os.path.join(output_folder_path, f'{foldername}-{metric}.csv')
        result_df.to_csv(output_file_path, index=False)
    #print(f"Mean {metric} saved")

# 指定CSV文件夹路径
csv_folder_path = os.path.join(os.getcwd(), 'data')

output_folder = 'whole-results'
output_folder_path = os.path.join(os.getcwd(), output_folder)
os.makedirs(output_folder_path, exist_ok=True)



# 调用函数处理不同的metric
for metric in metrics:
    process_metric(csv_folder_path, output_folder_path, metric)
print('whole.py finished')
