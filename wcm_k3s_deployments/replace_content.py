# function of this scipt: replace content in yaml files

import os
import re

def get_yaml_paths(folder_path):
    yaml_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(".yaml"):
            yaml_paths.append(os.path.join(folder_path, file))
    return yaml_paths


# 获取当前Python文件的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
# 输入文件夹路径
input_folder = script_dir # 输入文件夹

old_content = "/home/tumi6/autoware-microservice-bench/launch"
#old_content = "perception3_"
#old_content = "/home/tumi6/autoware-microservice-bench/autoware_log"

new_content = "/home/tumi6/workspace/autoware-microservice-bench/launch"
#new_content = "perception"
#new_content = "/home/tumi6/workspace/autoware-microservice-bench/autoware_log"

# get yaml file paths
yaml_paths = get_yaml_paths(input_folder)

for yaml_path in yaml_paths:
    with open(yaml_path, "r+") as yaml_file:
        content = yaml_file.read()
        updated_content = re.sub(old_content, new_content, content)
        yaml_file.seek(0)
        yaml_file.write(updated_content)
        yaml_file.truncate()

print("Change succeed")
