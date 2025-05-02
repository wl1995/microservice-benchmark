# Virtualization & Microservice Architecture for Software-Defined Vehicles: An Evaluation and Exploration

## 1. Introduction

This repository includes codes for autoware deployment and data process

**NOTE**: To properly use the deployment files for benchmarking, please replace all the paths like **/home/tumi6** to your own path.

**NOTE 2**: We have modified the source code of ROS2. Please copy the folders in ROS2_source_code and replace them in the ROS2 folder.

**NOTE 3**: The provided container image is a full image that contains all required dependencies for the whole Autoware. However eliminating the unnecessary contents for different module images can further boost the performance and start-up time. For detailed information about the minimum setups for each module, please refer to **eliminating.txt**. These setups are tested by ourself and optimizations may still be available.

## 2. File Structure

- **autoware_log**: k3s log files and k3s start up time process scripts *sorter.py, startup_time.py*
- **bash_folder**: bash files to run test *bare-metal-rosbag, k3s 17 pods, k3s 26 pods*
- **launch**: launch files
- **k3s_deployments**: k3s deployment files
- **test_result_process**: process test results
- **ROS2_source_code**: source code for tracing launch of nodes


## 3. Installation

### Autoware
   
   Extract from the compressed archive and install dependencies

   https://autowarefoundation.github.io/autoware-documentation/galactic/installation/autoware/source-installation/#source-installation

### ROS2_galactic

   ROS2 galactic need to be installed from source to ensure the launch of every node is reported. Debian install is also fine if you only want to have a try.
   
   **Important**: The **action** folder in **ROS2_source_code** need to be pased to ```/path/to/ros/ros2_galactic/src/ros2/launch_ros/launch_ros/launch_ros``` and the **rclcpp_components** folder need to be pased to ```/path/to/ros/ros2_galactic/src/ros2/rclcpp/rclcpp_components/include``` and then recompile the whole ROS2.

   To install dependencies of end-of-life distros 
   
   ```bash
   rosdep --include-eol-distros update
   ```

### Docker

   https://docs.docker.com/engine/install/ubuntu/

### K3s (runtime Docker)

   The default runtime of k3s is containerd, make sure using docker runtime when installing k3s.

   https://docs.k3s.io/advanced#using-docker-as-the-container-runtime

### NVIDIA Container Toolkit

   Installation and configuration

   https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation

   After you install and configure the toolkit and install an NVIDIA GPU Driver, you can verify your installation by running a sample workload.

   https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/sample-workload.html#running-a-sample-workload-with-docker

### NVIDIA device plugin for Kubernetes

   https://github.com/NVIDIA/k8s-device-plugin#enabling-gpu-support-in-kubernetes



## 4. K3s Deployment Workflow

Details in `k3s_deployments\README.md`

## 5. Data Processing Workflow

Details in `test_result_process\README.md`


