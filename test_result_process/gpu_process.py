'''
    For each test, extract CPU and RAM usage in whole process
    calculate the mean, standard deviation, minimum and maximum
'''
import pandas as pd
import os

def get_time(csv_folder_path, time_lens):
    for foldername in os.listdir(csv_folder_path):
        stats_path = os.path.join(csv_folder_path, foldername, 'cpu_mem_analysis/total')
        filename = 'CPU_sums.csv'
        csv_file_path = os.path.join(stats_path, filename)

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # Extract the desired columns
        data_column = df.iloc[:, 0]

        time_lens[foldername] = len(data_column)
        #print(f'{foldername}: {time_lens[foldername]}\n')


def gpu_process(csv_folder_path, output_folder_path, time_lens, metric):
    for foldername in os.listdir(csv_folder_path):
        stats_path = os.path.join(csv_folder_path, foldername)
        if os.path.isdir(stats_path):
            filename = 'gpu.csv'
            # 构建CSV文件的完整路径
            csv_file_path = os.path.join(stats_path, filename)

            # 读取CSV文件
            df = pd.read_csv(csv_file_path)

            gpu_column = df.iloc[:, 0]

            # Compare the lengths and pad with zeros if needed
            if len(gpu_column) < time_lens[foldername]:
                # Calculate the number of zeros to add
                zeros_to_add = time_lens[foldername] - len(gpu_column)
                # Add zeros at the beginning of the column
                gpu_column = [0] * zeros_to_add + list(gpu_column)

            # Create a DataFrame with the padded GPU column
            result_df = pd.DataFrame({metric: gpu_column})
            
            output_file_path = os.path.join(output_folder_path, foldername, 'cpu_mem_analysis/total', f'{metric}_sums.csv')
            result_df.to_csv(output_file_path, index=False)
    

# 指定CSV文件夹路径
csv_folder_path = os.path.join(os.getcwd(), 'data')

# save time of differnt tests
time_lens = {}
get_time(csv_folder_path, time_lens)

csv_folder_path = os.path.join(os.getcwd(), 'results')
output_folder_path = os.path.join(os.getcwd(), 'data')
os.makedirs(output_folder_path, exist_ok=True)


gpu_process(csv_folder_path, output_folder_path, time_lens, 'GPU')
print(f"gpu_process.py finished")

