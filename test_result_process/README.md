# Test Result Processing

## Collect Data

The test data collection process is detailed in the `benchmark_monitoring/README.md` file.

## Process Data

To process the collected data, follow these steps:

1. **Copy Scripts:**
   Copy all scripts from this folder to `benchmark_monitoring`.

2. **Create Conda Environment:**
   Create a conda environment and install the necessary dependencies listed in `requirements.txt`.

    ```bash
    conda create --name your_environment_name --file requirements.txt
    ```

3. **Activate Conda Environment:**
   Open a terminal and activate the conda environment.

    ```bash
    conda activate your_environment_name
    ```

4. **Run Data Processing Script:**
   Execute the data processing script within the conda environment.

    ```bash
    bash data_process.sh
    ```

## Result Explanation

Upon running `bash data_process.sh`, four folders will be generated:

### 1. whole-results

   This folder contains the results for each test, with three corresponding `.csv` files representing CPU, RAM, and GPU usage. Each `.csv` file includes four statistical values: mean, standard deviation, minimum, and maximum.

### 2. whole-mean-results

   Aggregate all test results within the same test scenario (e.g., *kvm-bare-metal*) and save the mean values for different tests.

### 3. whole-compared-results

   Establish a base scenario (*bare-metal-rosbag*) and calculate the percentage difference between each test scenario and the base scenario using the formula: `test_scenario / base_scenario * 100%`.

### 4. time-results

   This folder combines all test results within the same scenario (e.g., *kvm-bare-metal*). It additionally trims the data length in each test to ensure uniformity, resulting in datasets of the same length within
