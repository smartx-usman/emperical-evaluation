#!/bin/python3
import os
import re
import subprocess
import sys

# Define the intermediate input file names
input_files = ["clients100_requests10.txt", "clients100_requests500.txt", "clients100_requests1000.txt", "clients100_requests1500.txt"]

# Extract data from result file to individual files
command = (
    f"grep -w -A 4 'Clients: 100, Requests: 10' result.txt >> clients100_requests10.txt &&"
    f"grep -w -A 4 'Clients: 100, Requests: 500' result.txt >> clients100_requests500.txt &&"
    f"grep -w -A 4 'Clients: 100, Requests: 1000' result.txt >> clients100_requests1000.txt &&"
    f"grep -w -A 4 'Clients: 100, Requests: 1500' result.txt >> clients100_requests1500.txt"
)

# Run the command
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command failed
if result.returncode != 0:
    print("Command failed.")
    print("Error Output:")
    print(result.stderr)
    sys.exit(1)

# Read the content of the file
for i in (0, 1, 2, 3):
    with open(input_files[i], 'r') as file:
        text = file.read()

    # Use regular expressions to find all average latency values
    average_latencies = re.findall(r'Average Latency: ([\d.]+) seconds', text)
    average_throughput = re.findall(r'Throughput: ([\d.]+) requests/second', text)

    # Convert the found values to float and calculate the average
    average_latencies = [float(latency) for latency in average_latencies]
    average_latency = sum(average_latencies) / len(average_latencies)
    average_latency_sec = average_latency * 100

    average_throughput = [float(throughput) for throughput in average_throughput]
    average_throughput = sum(average_throughput) / len(average_throughput)

    if i == 0:
        print(f"Average Latency from all experiments[clients: 100 requests: 10]: {average_latency_sec:.2f} seconds")
        print(f"Average Throughput from all experiments[clients: 100 requests: 10]: {average_throughput:.2f} \n")
    elif i == 1:
        print(f"Average Latency from all experiments[clients: 100 requests: 500]: {average_latency_sec:.2f} seconds")
        print(f"Average Throughput from all experiments[clients: 100 requests: 500]: {average_throughput:.2f} \n")
    elif i == 2:
        print(f"Average Latency from all experiments[clients: 100 requests: 1000]: {average_latency_sec:.2f} seconds")
        print(f"Average Throughput from all experiments[clients: 100 requests: 1000]: {average_throughput:.2f} \n")
    else:
        print(f"Average Latency from all experiments[clients: 100 requests: 1500]: {average_latency_sec:.2f} seconds")
        print(f"Average Throughput from all experiments[clients: 100 requests: 1500]: {average_throughput:.2f} \n")

# Remove intermediate data files
for file_path in input_files:
    if os.path.exists(file_path):
        os.remove(file_path)
