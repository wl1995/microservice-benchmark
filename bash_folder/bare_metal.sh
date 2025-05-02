source /home/tumi6/autoware/install/setup.bash
echo "bare metal launched: $(date +"%T.%N")"  > /home/tumi6/workspace/autoware-microservice-bench/autoware_log/bare_log/bare_log.txt
ros2 launch autoware_launch logging_simulator.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit vehicle_id:=1 map_path:=$HOME/autoware_map/sample-map-rosbag >> /home/tumi6/workspace/autoware-microservice-bench/autoware_log/bare_log/bare_log.txt
