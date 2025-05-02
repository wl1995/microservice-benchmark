#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

echo "TUM launched map: $(date +"%T.%N")"

ros2 launch autoware_launch map.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit vehicle_id:=1 map_path:=$HOME/autoware_map/sample-map-rosbag
