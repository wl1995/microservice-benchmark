#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched control2: $(date +"%T.%N")"

ros2 launch autoware_launch control2.launch.py