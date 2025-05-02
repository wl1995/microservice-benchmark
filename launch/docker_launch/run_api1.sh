#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched API 1: $(date +"%T.%N")"

ros2 launch autoware_launch api1.launch.xml launch_api1:=true
