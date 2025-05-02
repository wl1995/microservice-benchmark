# File Structure

## sorter.py

Collect time information from log files, including:

1. Modules start time, end time, duration
2. K3s start time, end time, duration
3. K3s launch time

Save time information into the `sorted` folder.

## startup_time.py

Using the sorted results from `sorter.py`, calculate the average startup time and duration of each module, and save them into `startup.txt`.

# Workflow

1. Run the k3s deployment; the following logs will be saved into this folder:
    - K3s modules launch log
    - K3s launch timestamp log

2. Run the following scripts to process logs:

    ```bash
    python3 sorter.py
    python3 startup_time.py
    ```
