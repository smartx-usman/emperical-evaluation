#!/bin/bash

# Check for the number of command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <distribution> <node_type> <iterations> <wait_time>"
    echo "E.g., ./monitor-ps.sh microk8s master 10 5"
    echo "E.g., ./monitor-ps.sh k0s worker 50 5"
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

# Get the hostname for naming output files
host=$(hostname)

# Check if the output file already exists, then remove them
find "$HOME_PATH" -type f -name "pu_*" -exec rm {} \;

if [ "$node" = "worker" ]; then
  if [ "$distribution" = "microk8s" ]; then
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "kubelite|containerd|calico-node" | grep -E -v "containerd-shim" >> "pu_memory_${host}.txt" &
      pidstat -u -h -C "kubelite|containerd|calico-node" | grep -E -v "containerd-shim" >> "pu_cpu_${host}.txt" &
      sleep $wait_time
    done
  else
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "kubelet|containerd|k0s|konnectivity" | grep -E -v "containerd-shim" >> "pu_memory_${host}.txt" &
      pidstat -u -h -C "kubelet|containerd|k0s|konnectivity" | grep -E -v "containerd-shim" >> "pu_cpu_${host}.txt" &
      sleep $wait_time
    done
  fi
elif [ "$node" = "master" ]; then
  if [ "$distribution" = "microk8s" ]; then
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "k8s-dqlite|kubelite|calico-node" >> "pu_memory_${host}.txt" &
      pidstat -u -h -C "k8s-dqlite|kubelite|calico-node" >> "pu_cpu_${host}.txt" &
      sleep $wait_time
    done
  else
    for ((i = 1; i <= iterations; i++)); do
      pidstat -r -h -C "etcd|kube-apiserver|k0s|konnectivity" >> "pu_memory_${host}.txt" &
      pidstat -u -h -C "etcd|kube-apiserver|k0s|konnectivity" >> "pu_cpu_${host}.txt" &
      sleep $wait_time
    done
  fi
fi

echo "All the commands have completed. check output files."