#!/bin/bash

Red='\033[0;31m'
Green='\e[32m'
Yellow='\033[0;33m'
BBlue='\e[44m'

LOGFILE="./dp.log"
HOME_PATH="./data"

# Default values
result_file="result.txt"
coap_server="single"
coap_port="5683" # or 31839

handle_debug() {
  { set +x; } 2>/dev/null; echo -n "[$(date -Is)]  "; set -x
}

handle_error() {
  echo -e "\e[31mERROR: An error occurred during execution, check log $LOGFILE for details.\e[0m"
  exit 1
}

exec 3>&1 1>"$LOGFILE" 2>&1

set -ex # Prints commands, prefixing them with a character stored in an environmental variable ($PS4)
trap "handle_error" ERR
trap '{ set +x; } 2>/dev/null; echo -n "[$(date -Is)]  "; set -x' DEBUG

# Function to display usage information
usage() {
  echo "Usage: $0 [-f <result_file>] [-s <coap_server>] [-p <coap_port>]" >&3
  echo "  -f <result_file>: Specify the result file (default: result.txt)" >&3
  echo "  -s <coap_server>: Specify the CoAP server (default: single)" >&3
  echo "  -p <coap_port>: Specify the CoAP port (default: 5683)" >&3
  exit 1
}

# Parse command line arguments
while getopts ":f:s:p:" opt; do
  case $opt in
    f)
      result_file="$OPTARG"
      ;;
    s)
      coap_server="$OPTARG"
      ;;
    p)
      coap_port="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument."
      usage
      ;;
  esac
done

# Check if the file exists
if [ -e "$result_file" ]; then
  rm "$result_file"
fi

# Install CoAPthon3 library
pip3 install CoAPthon3

# Run experiments
for experiment in 1 2 3 4 5
do
  echo "[........... Experiment No. $experiment ..........]" >> $result_file
  # for clients in 1 100 200
  for clients in 100
  do
    for requests in 10 500 1000 1500
    do
      echo -e "$BBlue No. of clients: $clients, No. of requests: $requests" >&3
      taskset -c 1 python3 coap-stress.py $coap_server $coap_port $clients $requests $result_file
      echo -e "$BBlue Test completed. Sleeping for 30s..." >&3
      sleep 30
    done
  done
done
