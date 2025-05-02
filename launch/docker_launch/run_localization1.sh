#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched localization1: $(date +"%T.%N")"

ros2 launch autoware_launch localization1.launch.xml vehicle_model:=sample_vehicle launch_localization1:=true
