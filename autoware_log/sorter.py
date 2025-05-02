import os
import re
from datetime import datetime, timedelta

# input folder: log files
source_folder = os.getcwd()

target_folder = os.path.join(source_folder, "./sorted")
os.makedirs(target_folder, exist_ok=True)

# Find lines with time information
pattern = re.compile(r'\d{2}:\d{2}:\d{2}.\d{3}')

# Find module name
log_module_pattern = re.compile(r'log_([^0-9]+)\w*\.txt')


for folder_name in os.listdir(source_folder):
    folder_path = os.path.join(source_folder, folder_name)
    if os.path.isdir(folder_path) and 'log' in folder_name and not 'bare' in folder_name:
        # Path to save the sorted time information
        output_file = os.path.join(target_folder, f"sorted_{folder_name}.txt")

        with open(output_file, "w") as output_file:
            time_differences = {}
            for root, dirs, files in os.walk(folder_path):
                sorted_files = sorted(files)
                for file in sorted_files:
                    # Here, input path indicates each log file '.txt' 
                    input_path = os.path.join(root, file)
                    with open(input_path, "r") as input_file:
                        output_file.writelines('\n' + input_path + '\n')
                        lines = input_file.readlines()
                        # Extract lines with time information
                        filtered_lines = [line for line in lines if pattern.search(line)]
                        # Sort lines by time order
                        sorted_lines = sorted(filtered_lines, key=lambda line: datetime.strptime(pattern.search(line).group(), '%H:%M:%S.%f'))
                        # Find the first time stamp and last time in this log file
                        first_timestamp = datetime.strptime(pattern.search(sorted_lines[0]).group(), '%H:%M:%S.%f')
                        last_timestamp = first_timestamp
                        for line in sorted_lines:
                            current_timestamp = datetime.strptime(pattern.search(line).group(), '%H:%M:%S.%f')
                            #filter timestamps after 10 seconds
                            if((current_timestamp - first_timestamp).total_seconds() < 10):
                                last_timestamp = current_timestamp
                            else:
                                break
                            
                        time_difference = (last_timestamp - first_timestamp).total_seconds()
                        
                        output_file.write(f"Time Difference: {time_difference}\n")

                        log_module_match = log_module_pattern.search(file)
                        if log_module_match:
                            module_name = log_module_match.group(1)
                            if(module_name in time_differences):
                                start_time = min(first_timestamp, time_differences[module_name][0])
                                end_time = max(last_timestamp, time_differences[module_name][1]) 
                                time_differences[module_name] = (start_time, end_time)
                            else:
                                time_differences[module_name] = (first_timestamp, last_timestamp)

                        output_file.writelines(sorted_lines)

            output_file.writelines("\nLaunch time(seconds) for modules: \n")    
            k3s_start = None
            k3s_end = None
            for module_name, (start_time, end_time) in time_differences.items():
                time_difference = (end_time - start_time).total_seconds()
                start_time_str = start_time.strftime('%H:%M:%S.%f')[:-3]
                end_time_str = end_time.strftime('%H:%M:%S.%f')[:-3]
                k3s_start = min(k3s_start, start_time) if k3s_start is not None else start_time
                k3s_end = max(k3s_end, end_time) if k3s_end is not None else end_time
                output_file.writelines(f"{module_name.ljust(20)} \tStart : {start_time_str} \tEnd: {end_time_str} \tDuration: {time_difference}\n")
            
            k3s_start_str = k3s_start.strftime('%H:%M:%S.%f')[:-3]
            k3s_end_str = k3s_end.strftime('%H:%M:%S.%f')[:-3]
            k3s_total = (k3s_end - k3s_start).total_seconds()
            output_file.writelines(f"{'k3s'.ljust(20)} \tStart : {k3s_start_str} \tEnd: {k3s_end_str} \tDuration: {k3s_total}\n")
            

# Get the k3s launch start time
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)
    if 'txt' in file_name:
        k3s_launch_time_path = file_path
        output_file = os.path.join(target_folder, f"sorted_{file_name}")

        with open(k3s_launch_time_path, "r") as k3s_launch_time_file, open(output_file, "a+") as output_file:
            content = k3s_launch_time_file.read()
            output_file.write(content)

            output_file.seek(0)
            lines = output_file.readlines()
            
            # Second last line is k3s module start time
            second_last_line = lines[-2].strip()
            second_last_timestamps = re.findall(pattern, second_last_line)
            k3s_start_timestamp = datetime.strptime(second_last_timestamps[0], '%H:%M:%S.%f')

            # Last line is k3s launch start time
            last_line = lines[-1].strip()
            # Time in k3s in 1 hour later than in system time, i.e. (k3s launch time - k3s start time > 1h)
            k3s_launch_timestamp = datetime.strptime(pattern.search(last_line).group(), '%H:%M:%S.%f') - timedelta(hours=1)

            # Calculate the launch duration and write to file
            launch_duration = (k3s_start_timestamp - k3s_launch_timestamp).total_seconds()
            output_file.write(f"K3s launch time: {launch_duration:.3f} seconds\n")

            k3s_launch_str = k3s_launch_timestamp.strftime('%H:%M:%S.%f')[:-3]
            k3s_start_str = k3s_start_timestamp.strftime('%H:%M:%S.%f')[:-3]
            output_file.writelines(f"{'k3s_launch'.ljust(20)} \tStart : {k3s_launch_str} \tEnd: {k3s_start_str} \tDuration: {launch_duration}\n")

            total_end_timestamp = datetime.strptime(second_last_timestamps[-1], '%H:%M:%S.%f')
            total_duration = (total_end_timestamp - k3s_launch_timestamp).total_seconds()
            total_start_str = k3s_launch_str
            total_end_str = second_last_timestamps[-1]
            output_file.writelines(f"{'total'.ljust(20)} \tStart : {total_start_str} \tEnd: {total_end_str} \tDuration: {total_duration}\n")


print("Data saved successfully!")
