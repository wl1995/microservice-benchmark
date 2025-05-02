#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched perception3: $(date +"%T.%N")"

ros2 launch autoware_launch perception1.launch.xml vehicle_model:=sample_vehicle launch_perception3:=true