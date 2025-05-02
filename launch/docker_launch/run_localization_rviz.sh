#!/bin/bash
export ROS_DOMAIN_ID=5  
    
source /opt/ros/galactic/setup.bash
source /autoware/install/setup.bash

export DISPLAY=:0
#Xvfb $DISPLAY -screen 0 1024x768x16 &
#gnome-terminal -- bash -c "/usr/games/nudoku"
#x11vnc -display $DISPLAY -forever -nopw -quiet -listen localhost -xkb
#export DISPLAY=${DISPLAY:-:0} # Select screen 0 by default.
xdpyinfo
if which x11vnc &>/dev/null; then
          ! pgrep -a x11vnc && x11vnc -bg -forever -nopw -quiet -display WAIT$DISPLAY &
fi
! pgrep -a Xvfb && Xvfb $DISPLAY -screen 0 3840x2160x16 &

echo "TUM launched localization: $(date +"%T.%N")"

ros2 launch autoware_launch localization_rviz.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit vehicle_id:=1 map_path:=$HOME/autoware_map/sample-map-rosbag
