#!/bin/bash

# Check for the number of command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <process_name> <distribution> <iterations> <wait_time>"
    echo "E.g., ./monitor.sh microk8s mater 10 5"
    exit 1
fi

HOME_PATH="/home/aida"

# Check type of the distribution
distribution=$1

# Check type of the node
node=$2

# Number of iterations
iterations=$3

# Wait time between each run (in seconds)
wait_time=$4

# Check if the output file already exists, then remove them
find "$HOME_PATH" -type f -name "pu_*" -exec rm {} \;

if [ "$node" = "worker1" ]; then
  if [ "$distribution" = "microk8s" ]; then
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "kubelite|containerd|calico-node" | grep -E -v "containerd-shim" >> pu_memory_worker1.txt &
      pidstat -u -h -C "kubelite|containerd|calico-node" | grep -E -v "containerd-shim" >> pu_cpu_worker1.txt &
      sleep $wait_time
    done
  else
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "kubelet|containerd" | grep -E -v "containerd-shim" >> pu_memory_worker1.txt &
      pidstat -u -h -C "kubelet|containerd" | grep -E -v "containerd-shim" >> pu_cpu_worker1.txt &
      sleep $wait_time
    done
  fi
elif [ "$node" = "master" ]; then
  if [ "$distribution" = "microk8s" ]; then
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "k8s-dqlite|kubelite|calico-node" >> pu_memory_master.txt &
      pidstat -u -h -C "k8s-dqlite|kubelite|calico-node" >> pu_cpu_master.txt &
      sleep $wait_time
    done
  else
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "etcd|kube-apiserver" >> pu_memory_master.txt &
      pidstat -u -h -C "etcd|kube-apiserver" >> pu_cpu_master.txt &
      sleep $wait_time
    done
  fi
else
  echo "Invalid argument. Exiting for now."
  echo "Please enter the command in format: ./monitor.sh distribution node iterations wait"
  echo "E.g., ./monitor-ps.sh k0s master 10 5"
  exit 1
fi

echo "All the commands have completed. check output files."