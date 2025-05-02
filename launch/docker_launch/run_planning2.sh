#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched planning2: $(date +"%T.%N")"

ros2 launch autoware_launch planning1.launch.xml vehicle_model:=sample_vehicle launch_planning2:=true
