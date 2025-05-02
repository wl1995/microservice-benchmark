# Launch scenarios

## Bare metal:

  Open one terminal

  ```bash
  source ~/autoware/install/setup.bash

  ros2 launch autoware_launch logging_simulator.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit vehicle_id:=1 map_path:=/home/tumi6/autoware_map/sample-map-rosbag
  ```

  Open another terminal

  ```bash
  source ~/autoware/install/setup.bash

  ros2 bag play /home/tumi6/autoware_map/sample-rosbag/sample.db3 -r 0.2 -s sqlite3
  ```

## Docker

  ```bash
  docker run -it --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all -p 5900:5900 autoware-whole-time ./run_autoware.sh

  vncviewer localhost:5900

  docker run -it autoware-rosbag ./run_rosbag.sh
  ```

## K3s run whole system

  ```bash
  kubectl apply -f ./wcm-whole-norosbag.yaml

  vncviewer localhost:31005

  kubectl apply -f ./wcm-rosbag.yaml
  ```

## K3s run 10 pods

  ```bash
  kubectl apply -f ./wcm-modules.yaml

  vncviewer localhost:31004
  ```


## K3s, divide perception into 4 parts

1. Find all parameters in `logging_simulator.launch.xml` and `autoware.launch.xml`, which are necessary to launch perception. Copy them into `perception1.launch.xml`.
2. Copy `perception.launch.xml` into the launch file we created above.
3. Delete duplicate parameters, make sure all parameters can be found in this launch file
4. In `run_perception1.sh`, launch `perception1.launch.xml`, pass parameter `vehicle_model:=sample_vehicle`.
5. Divide module into 4 parts, every part has a parameter `launch_perception`, by passing the paramter value we can decide which part to launch

  ```bash
  kubectl apply -f ./wcm-perc.yaml

  vncviewer localhost:31004

  kubectl apply -f ./wcm-rosbag.yaml
  ```


## K3s, divide Planning

1. Mission planning, 2 nodes
2. Scenario_planning, 3 sub modules:
    - scenario selector: 1 node
    - velocity planning: 2 nodes
    - scenarios: 13 nodes
3. Error monitor: 1 node

**Error: In velocity planning**

  ```
  [motion_velocity_smoother-2] [ERROR] [1698061241.800603325] [planning.scenario_planning.motion_velocity_smoother]: Failed to get parameter `wheel_radius`, please set it when you launch the node.
  ```

**Solution**
* Add the following part from `autoware.launch.xml` into `planning1.launch.xml`, error solved, probably the parameter needed is in this module

  ```
  <!-- Global parameters -->
  <group scoped="false">
    <include file="$(find-pkg-share global_parameter_loader)/launch/global_params.launch.py">
      <arg name="use_sim_time" value="false"/>
      <arg name="vehicle_model" value="$(var vehicle_model)"/>
    </include>
  </group>
  ```

  ```bash
  kubectl apply -f ./wcm-plan.yaml

  vncviewer localhost:31004

  kubectl apply -f ./wcm-rosbag.yaml
  ```


## K3s, divide Sensing

1. LiDAR 
    1. top
    2. left
    3. right
    4. rear
    5. pointcloud_preprocessor
2. IMU Driver
3. GNSS Driver
4. Vehicle Velocity Converter

  ```bash
  kubectl apply -f ./wcm-sens.yaml

  vncviewer localhost:31004

  kubectl apply -f ./wcm-rosbag.yaml
  ```

## K3s, divide Api


  ```bash
  kubectl apply -f ./wcm-api.yaml

  vncviewer localhost:31004

  kubectl apply -f ./wcm-rosbag.yaml
  ```

## K3s, divide Localization

  ```bash
  kubectl ./wcm-localization.yaml

  vncviewer localhost:31004

  kubectl ./wcm-rosbag.yaml
  ```


## K3s, final deployment, 26 pods

  ```bash
  kubectl apply -f ./wcm-final.yaml

  vncviewer localhost:31004
  ```

## K3s, final deployment, 17 pods

  ```bash
  kubectl apply -f ./wcm-final-17.yaml

  vncviewer localhost:31004
  ```


# Troubleshooting
  
**Error in Rviz**
**Solutions**
  1. When we modify autoware.launch.xml, we deleted `web controller` and `api`, so that Rviz can't be launched
  2. In `run_rviz.sh`, need to add the following code, to make sure the rviz has port to output
      ```bash
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
      ```



# Modules, Functions, Nodes

K3s run 17 or 26 pods

| Module | Functions | Nodes |
|---------|---------|---------|
| Vehicle | robot_state_publisher | 1 |
| System | system_monitor, ad_service_state_monitor, system_error_monitor, emergency_handler | 12 |
| Sensing | lidar 1-4, IMU_driver, GNSS_driver, Velocity_converter | 29 |
| Planning | Mission_planning, Scenario_selector, Velocity_planning, Scenario_library, planning_error_monitor | 17 |
| Perception | obstacle_segmentation, occupancy_grid_map, object_recognition, traffic_light_recognition | 28 |
| Map | map_loader | 6 |
| Location | pose_estimator, twist_estimator, pose_twist_fusion_filter, localization_error_monitor | 12 |
| Control | trajectory_follower, shift_decider, vehicle_cmd_gate, operation_mode_transition_manager, external_cmd_selector, external_cmd_converter | 8 |
| Api | AD_API, awapi_awiv_adapter, API_adaptor, API_utils, Rosbridge, Web_controller | 62 |
| Rviz | Visualization | 1 |

sum: 176 nodes

bare-metal: 189 nodes

