#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched control1: $(date +"%T.%N")"

ros2 launch autoware_launch control1.launch.py