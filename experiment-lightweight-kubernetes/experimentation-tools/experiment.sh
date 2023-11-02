#!/bin/bash

# include configurator script
source ./configurator.sh

# Check for the number of command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <operation> <object_type> <no_of_workers> <repetitions>"
    echo "E.g., ./experiment.sh create deployment 1 0"
    echo "E.g., ./experiment.sh all pods 3 2"
    exit 1
fi

# Command line arguments
operation=$1
type=$2
workers=$3
repetitions=$4

# Create output directory
let "total_runs = repetitions + 1"
OUTPUT_PATH="${BASE_PATH}/usman/${type}_${workers}worker_${total_runs}run"

# Check if the output directory exists, and create it if it doesn't
if [ ! -d "$OUTPUT_PATH" ]; then
    mkdir -p "$OUTPUT_PATH"
    echo -e "$Yellow Output Directory '$OUTPUT_PATH' created." >&3
else
    rm -rf "$OUTPUT_PATH/*"
    echo -e "$Yellow Output Directory '$OUTPUT_PATH' already exists." >&3
fi

# Define an array of remote hosts
REMOTE_HOSTS=("master" "worker1" "worker2" "worker3")

# Loop through the remote hosts and execute the monitoring command on each host
if [ "$workers" = 1 ]; then
  for ((i = 0; i < 2; i++))
  do
      COMMAND="rm -rf su_${REMOTE_HOSTS[i]}.txt && sar -u -r -d -n DEV 5 $execute_count > su_${REMOTE_HOSTS[i]}.txt"
      ssh -f -n "${REMOTE_HOSTS[i]}" "$COMMAND"
      # Optionally, capture the PID of the background process
      BG_PID=$!
      echo "Background process PID on $host: $BG_PID"
      #break
  done
else
  for host in "${REMOTE_HOSTS[@]}"; do
      COMMAND="rm -rf su_$host.txt && sar -u -r -d -n DEV 5 $execute_count > su_$host.txt"
      ssh -f -n "$host" "$COMMAND"
      BG_PID=$!
      echo "Background process PID on $host: $BG_PID"
      #((host_index++))
  done
fi

# System monitoring for idle
echo -e "$Yellow Waiting for $monitoring_wait seconds to measure idle usage." >&3
sleep $monitoring_wait

# Determine the number of pods/deployments to create
#deployment_file="./config/default/coap-${type}-${workers}worker.yaml"
deployment_file="./config/default/coap-${type}-object.yaml"

if [ "$type" = "pod" ] && [ "$workers" = 1 ]; then
  objects=(1 2 4 8 16 32 60 64)
  if [ "$operation" = "create" ]; then
    objects=(60)
  fi
  cp "${BASE_PATH}/${CONFIG_PATH}/coap-${type}.yaml" "${BASE_PATH}/${CONFIG_PATH}/coap-${type}-object.yaml"
elif  [ "$type" = "pod" ] && [ "$workers" = 3 ]; then
  objects=(1 2 4 8 16 32 60 64)
  if [ "$operation" = "create" ]; then
    objects=(120)
  fi
  yq e 'del(.spec.nodeSelector)' "${BASE_PATH}/${CONFIG_PATH}/coap-${type}.yaml" > "${BASE_PATH}/${CONFIG_PATH}/coap-${type}-object.yaml"
elif [ "$type" = "deployment" ] && [ "$workers" = 1 ]; then
  objects=(1 2 4 8 16 20 32)
  if [ "$operation" = "create" ]; then
    objects=(20)
  fi
  cp "${BASE_PATH}/${CONFIG_PATH}/coap-${type}.yaml" "${BASE_PATH}/${CONFIG_PATH}/coap-${type}-object.yaml"
elif  [ "$type" = "deployment" ] && [ "$workers" = 3 ]; then
  objects=(1 2 4 8 16 20 32 40)
  if [ "$operation" = "create" ]; then
    objects=(40)
  fi
  yq e 'del(.spec.nodeSelector)' "${BASE_PATH}/${CONFIG_PATH}/coap-${type}.yaml" > "${BASE_PATH}/${CONFIG_PATH}/coap-${type}-object.yaml"
else
  echo "Invalid argument. Please enter correct number of workers."
  exit 1
fi

if [ "$type" = "pod" ]; then
  for object in "${objects[@]}"
  do
    echo -e "$BBlue Starting experiment on ${workers} worker(s) for ${object} ${type}(s)" >&3

    jq --arg new_count "$object" '.Operations[0].Pods.Count = ($new_count | tonumber)' "${CONFIG_PATH}/base_${operation}_${type}.json" > temp1.json
    jq --arg new_runs "$repetitions" '.Operations[0].RepeatTimes = ($new_runs | tonumber)' temp1.json > temp2.json
    jq --arg new_deployment "$deployment_file" '.Operations[0].Pods.Actions[0].Spec.YamlSpec = ($new_deployment | tostring)' temp2.json > temp1.json
    mv temp1.json "${CONFIG_PATH}/kbench_config.json"

    kbench -kubeconfig /var/snap/microk8s/current/credentials/client.config -benchconfig "${CONFIG_PATH}/kbench_config.json" -outdir $OUTPUT_PATH
    #kbench -benchconfig config/default/base_pod_1worker_config.json -outdir $OUTPUT_PATH

    mv "${OUTPUT_PATH}/kbench.log" "${OUTPUT_PATH}/${object}${type}.log"

    echo -e "$BBlue Ending experiment with ${object} ${type}(s)" >&3
    echo -e "$Yellow Waiting for 60 seconds to clean up." >&3
    sleep 60
  done
elif [ "$type" = "deployment" ]; then
  for object in "${objects[@]}"
  do
    echo -e "$BBlue Starting experiment on ${workers} worker(s) for ${object} ${type}(s)" >&3

    jq --arg new_count "$object" '.Operations[0].Deployments.Count = ($new_count | tonumber)' "${CONFIG_PATH}/base_${operation}_${type}.json" > temp1.json
    jq --arg new_runs "$repetitions" '.Operations[0].RepeatTimes = ($new_runs | tonumber)' temp1.json > temp2.json
    jq --arg new_deployment "$deployment_file" '.Operations[0].Deployments.Actions[0].Spec.YamlSpec = ($new_deployment | tostring)' temp2.json > temp1.json
    mv temp1.json "${CONFIG_PATH}/kbench_config.json"

    kbench -kubeconfig /var/snap/microk8s/current/credentials/client.config -benchconfig "${CONFIG_PATH}/kbench_config.json" -outdir $OUTPUT_PATH
    mv "${OUTPUT_PATH}/kbench.log" "${OUTPUT_PATH}/${object}${type}.log"

    echo -e "$BBlue Ending experiment with ${object} ${type}(s)" >&3
    echo -e "$Yellow Waiting for 60 seconds to clean up." >&3
    sleep 60
  done
fi

# Wait for few more minutes before removing monitoring process
echo -e "$Yellow Waiting for $monitoring_wait seconds to clean up monitoring jobs." >&3
sleep $monitoring_wait

# Loop through the remote hosts and remove monitoring process and copy files
if [ "$workers" = 1 ]; then
  for ((i = 0; i < 2; i++)); do
      ssh "${REMOTE_HOSTS[i]}" "pkill sar || true"
      scp -r "${REMOTE_HOSTS[i]}:su_${REMOTE_HOSTS[i]}.txt"  $OUTPUT_PATH
      #break
  done
else
  for host in "${REMOTE_HOSTS[@]}"; do
      ssh "${host}" "pkill sar || true"
      scp -r "${host}:su_${host}.txt"  $OUTPUT_PATH
  done
fi

# Copy system usage file to the directory


echo -e "$BBlue All experiments are completed. Exiting Normally." >&3