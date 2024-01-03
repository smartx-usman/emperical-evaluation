#!/bin/bash

# include configurator script
source ./configurator.sh

# Check for the number of command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <kubernetes_distribution> <object_type> <no_of_workers> <experiment_repetitions>"
    echo "E.g., ./ps-experiment.sh microk8s pod 1 0"
    echo "E.g., ./ps-experiment.sh microk8s deployment 3 3"
    exit 1
fi

distribution=$1
type=$2
workers=$3
repetitions=$4

LOCAL_SCRIPT="${BASE_PATH}/monitor-ps.sh"

# Create output directory
let "total_runs = repetitions + 1"
OUTPUT_PATH="${BASE_PATH}/usman/pu_${workers}worker_${total_runs}run"

# Check if the output directory exists, and create it if it doesn't
if [ ! -d "$OUTPUT_PATH" ]; then
    mkdir -p "$OUTPUT_PATH"
    echo -e "$Yellow Output Directory '$OUTPUT_PATH' created." >&3
else
    rm -rf "$OUTPUT_PATH/*"
    echo -e "$Yellow Output Directory '$OUTPUT_PATH' already exists." >&3
fi

# Define an array of remote hosts
if [ "$distribution" = "microshift" ]; then
  REMOTE_HOSTS=("master")
else
  REMOTE_HOSTS=("master" "worker1")
fi

# Loop through the remote hosts and execute the monitoring command on each host
if [ "$workers" = 1 ]; then
  for ((i = 0; i < 2; i++))
  do
      host="${REMOTE_HOSTS[i]}"

      # Determine the mode (master or worker) of the host
      if [[ $host =~ [0-9]$ ]]; then
          mode="${host%?}"
      else
        mode="${host}"
      fi

      ssh -f -n "${host}" "bash ~/$(basename $LOCAL_SCRIPT) $distribution $mode $execute_count 5"

      # Microshift has just one node and no worker nodes.
      if [ "$distribution" = "microshift" ]; then
        break
      fi
  done
else
  for host in "${REMOTE_HOSTS[@]}"; do
      # Determine the mode (master or worker) of the host
      if [[ $host =~ [0-9]$ ]]; then
          mode="${host%?}"
      else
        mode="${host}"
      fi

      ssh -f -n "$host" "bash ~/$(basename $LOCAL_SCRIPT) $distribution $mode $execute_count 5"
  done
fi

# System monitoring for idle
echo -e "$Yellow Waiting for $monitoring_wait seconds to measure idle usage." >&3
sleep $monitoring_wait

# Determine the configuration files to use
deployment_file="./config/default/coap-${type}-object.yaml"
cp "${BASE_PATH}/${CONFIG_PATH}/coap-${type}.yaml" "${BASE_PATH}/${CONFIG_PATH}/coap-${type}-object.yaml"

# Determine the number of pods/deployment to create
if [ "$workers" = 1 ]; then
  experiments=(60)
elif [ "$workers" = 3 ]; then
  experiments=(180)
else
  echo "Invalid argument. Please enter correct number of workers."
  exit 1
fi

for experiment in "${experiments[@]}"
do
  echo -e "$BBlue Starting experiment on ${workers} worker(s) for ${experiment} Pod(s)" >&3

  jq --arg new_count "$experiment" '.Operations[0].Pods.Count = ($new_count | tonumber)' "${CONFIG_PATH}/base_all_pod.json" > temp1.json
  jq --arg new_runs "$repetitions" '.Operations[0].RepeatTimes = ($new_runs | tonumber)' temp1.json > temp2.json
  jq --arg new_deployment "$deployment_file" '.Operations[0].Pods.Actions[0].Spec.YamlSpec = ($new_deployment | tostring)' temp2.json > temp1.json
  mv temp1.json "${CONFIG_PATH}/kbench_config.json"

  #kbench -kubeconfig /var/snap/microk8s/current/credentials/client.config -benchconfig "${CONFIG_PATH}/kbench_config.json" -outdir $OUTPUT_PATH
  kbench -benchconfig "${CONFIG_PATH}/kbench_config.json" -outdir $OUTPUT_PATH
  mv "${OUTPUT_PATH}/kbench.log" "${OUTPUT_PATH}/${experiment}pod.log"

  echo -e "$BBlue Ending experiment with ${experiment} Pod(s)" >&3
  echo -e "$Yellow Waiting for 60 seconds to clean up." >&3
  sleep 60
done

# Wait for few more minutes before removing monitoring process
echo -e "$Yellow Waiting for $monitoring_wait seconds to clean up monitoring jobs." >&3
sleep $monitoring_wait

# Loop through the remote hosts and remove monitoring process
COMMAND="pkill -f monitor-ps.sh || true"

if [ "$workers" = 1 ]; then
  for ((i = 0; i < 2; i++)); do
    if ssh "${REMOTE_HOSTS[i]}" "$COMMAND"; then
      #ssh "${REMOTE_HOSTS[i]}" "$COMMAND"
      echo "pkill command executed successfully"
    else
      echo "pkill command returned a non-zero exit code, but the script continues."
    fi
      scp -r "${REMOTE_HOSTS[i]}:pu_*" $OUTPUT_PATH
  done
else
  for host in "${REMOTE_HOSTS[@]}"; do
    #ssh "${host}" "$COMMAND"
    if ssh "${host}" "$COMMAND"; then
    #ssh "${REMOTE_HOSTS[i]}" "$COMMAND"
      echo "pkill command executed successfully"
    else
      echo "pkill command returned a non-zero exit code, but the script continues."
    fi
      scp -r "${host}:pu_*" $OUTPUT_PATH
  done
fi

# Check if the file exists
if [ -e "temp2.json" ]; then
  rm "temp2.json" "$CONFIG_PATH/kbench_config.json"
fi

echo -e "$BBlue All experiments are completed. Exiting Normally." >&3
