#!/bin/bash

# Check if the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root to gather all required information."
  exit 1
fi

if test "$#" -lt 1; then
	echo "Please specify experiment name"
	exit 22
fi

experiment_name=$1

rosbag=true

if [[ $experiment_name == *"planning"* ]]; then
    rosbag=false
elif [[ $experiment_name == *"rosbag"* ]]; then
    rosbag=true
else
	echo "Experiment name should contain simulation type"
	exit 22
fi

echo "Starting for experiment '$experiment_name'"

if [ $rosbag == true ]; then
	echo "Measuring gpu"
fi

# Create the "tmp" folder if it doesn't exist
if [[ ! -d "tmp" ]]; then
  mkdir tmp
fi

# Initialize counter variable
counter=0
experiment_start=0

# Function to measure CPU and Memory usage of each process
measure_cpu_memory() {
  ps -eo pid,%cpu,%mem,cmd --sort=-%cpu | sed 's/  */;/g' > "tmp/cpu_memory_${counter}.csv"
}

measure_gpu_memory() {
  nvidia-smi > "tmp/gpu_memory_${counter}.csv"
}

# Function to handle SIGINT signal and exit gracefully
function cleanup() {
  experiment_end=$((SECONDS))
  local timestamp=$(date +"%Y%m%d_%H%M%S")
  local folder_name="monitoring_results_${timestamp}"
  local destination_folder="data/$experiment_name/$folder_name"
  echo "Monitoring stopped. Copy Data..."
  mkdir -p "$destination_folder"  # Create the new folder inside the "data" folder
  cp -r tmp/* "$destination_folder/"  # Copy the contents of tmp folder into the new folder
  echo "Data copied into $destination_folder. Exiting..."
  rm -r tmp  # Remove the monitoring_results folder
  echo -e "timestamps,seconds\n$counter,$((experiment_end - experiment_start))" > "data/$experiment_name/duration.txt"
  exit 0
}

# Set up the trap to catch SIGINT signal (Ctrl + C)
trap cleanup SIGINT

# Main function for continuous monitoring
main() {
  end=$((SECONDS+600))  # End time (current time + 600 seconds)
  echo "Monitoring processes..."
  experiment_start=$((SECONDS))
  while [ $SECONDS -lt $end ]; do
    measure_cpu_memory
    if [ $rosbag == true ]; then
      measure_gpu_memory
    fi
    counter=$((counter+1))  # Increment the counter
    sleep 1.0
  done
  cleanup
}

# Call the main function
main
