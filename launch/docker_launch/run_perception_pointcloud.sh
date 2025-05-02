#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched perception_pointcloud: $(date +"%T.%N")"

ros2 launch autoware_launch pointcloud_container.launch.py use_multithread:=true container_name:=pointcloud_container