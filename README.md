# Containerizing ROS: Efficient Deployment and Management of Robotic Applications

## 1. Introduction

This repository includes codes for autoware deployment and data process

## 2. File Structure

- **autoware_log**: k3s log files and k3s start up time process scripts *sorter.py, startup_time.py*
- **bash_folder**: bash files to run test *bare-metal-rosbag, k3s 17 pods, k3s 26 pods*
- **launch**: launch files
- **original_k3s_deployments**: k3s deployment files, created before, not included in this thesis
- **wcm_k3s_deployments**: k3s deployment files
- **test_result_process**: process test results


## 3. Installation

### Autoware
   
   Extract from the compressed archive and install dependencies

   https://autowarefoundation.github.io/autoware-documentation/galactic/installation/autoware/source-installation/#source-installation

### ROS2_galactic

   Extract from the compressed archive

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

Details in `wcm_k3s_deployments\README.md`

## 5. Data Processing Workflow

Details in `test_result_process\README.md`


