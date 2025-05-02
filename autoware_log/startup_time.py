import os
import re
from datetime import datetime, timedelta

source_folder = os.path.join(os.getcwd(), 'sorted')

output_file = os.path.join(source_folder, "./startup.txt")
log_files = sorted([file_name for file_name in os.listdir(source_folder) if 'log' in file_name])

#modules = ['k3s_launch', 'vehicle', 'system', 'map', 'sensing', 'localization', 'perception', 'planning', 'control', 'api', 'rviz', 'total']
modules = ['k3s_launch', 'map', 'sensing', 'localization', 'planning', 'api', 'total']
first_17_start = {}
first_26_start = {}
first_5_start = {}
re_17_start = {}
re_26_start = {}
re_5_start = {}

first_17_duration = {}
first_26_duration = {}
first_5_duration = {}
re_17_duration = {}
re_26_duration = {}
re_5_duration = {}


# Find lines with time information
launch_pattern = re.compile(r'k3s launched\s*:\s*(\d{2}:\d{2}:\d{2}.\d{3})')
duration_pattern = re.compile(r'(\w+)\s+Start\s*:\s*(\S+)\s+End\s*:\s*(\S+)\s+Duration:\s*(\d+\.\d+)')

# Duration of each module
module_start = {}
module_durations = {}


with open(output_file, "w") as output_file:
    for file_name in log_files:
        file_path = os.path.join(source_folder, file_name)
        input_path = file_path
        
        if 'first_17' in file_name:
            module_start = first_17_start
            module_durations = first_17_duration
        elif 'first_26' in file_name:
            module_start = first_26_start
            module_durations = first_26_duration
        elif 'first_5' in file_name:
            module_start = first_5_start
            module_durations = first_5_duration
        elif 're_17' in file_name:
            module_start = re_17_start
            module_durations = re_17_duration
        elif 're_26' in file_name:
            module_start = re_26_start
            module_durations = re_26_duration
        elif 're_5' in file_name:
            module_start = re_5_start
            module_durations = re_5_duration

        with open(input_path, "r") as input_file:
            #output_file.writelines('\n' + input_path + '\n')
            lines = input_file.readlines()
            # find k3s launch command timestamp
            filtered_lines = [line for line in lines if launch_pattern.search(line)]
            #output_file.writelines(filtered_lines)
            for line in filtered_lines:
                launch_match = launch_pattern.search(line)
                if launch_match:
                    start_time = datetime.strptime(launch_match.group(1), '%H:%M:%S.%f')
                    # Time in k3s in 1 hour later than in system time
                    module_start['launch'] = start_time - timedelta(hours=1)


            # Find line with duration
            filtered_lines = [line for line in lines if duration_pattern.search(line)]
            #output_file.writelines(filtered_lines)
            for line in filtered_lines:
                duration_match = duration_pattern.match(line)
                if duration_match:
                    module_name, start_time, end_time, duration_value = duration_match.groups()
                    start_time = datetime.strptime(start_time, '%H:%M:%S.%f')
                    start_diff = (start_time - module_start['launch']).total_seconds()
                    duration_value = float(duration_value)
                    if module_name not in module_durations:
                        module_start[module_name] = 0.0
                        module_durations[module_name] = 0.0
                    module_start[module_name] += start_diff
                    module_durations[module_name] += duration_value


    
    output_file.writelines("\nAverage start time of each module: \n")
    for category, category_dict in [('first_17', first_17_start), ('first_26', first_26_start),('first_5', first_5_start), ('re_17', re_17_start), ('re_26', re_26_start),('re_5', re_5_start)]:
        output_file.writelines(f"\nCategory: {category}\n")
        for module_name in modules:
            category_dict[module_name] /= 5
            output_file.writelines(f"{module_name.ljust(25)} Start Time: {category_dict[module_name]:.3f}\n")

    output_file.writelines("\nAverage duration of each module: \n")
    for category, category_dict in [('first_17', first_17_duration), ('first_26', first_26_duration),('first_5', first_5_duration), ('re_17', re_17_duration), ('re_26', re_26_duration),('re_5', re_5_duration)]:
        output_file.writelines(f"\nCategory: {category}\n")
        for module_name in modules:
            output_file.writelines(f"{module_name.ljust(25)} Duration: {(category_dict[module_name] / 5):.3f}\n")



print("Data saved successfully!")
