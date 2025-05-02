#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched sensing2: $(date +"%T.%N")"

ros2 launch autoware_launch sensing1.launch.xml vehicle_model:=sample_vehicle vehicle_id:=1 launch_sensing2:=true