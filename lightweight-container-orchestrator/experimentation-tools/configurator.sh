#!/bin/bash

Red='\033[0;31m'
Green='\e[32m'
Yellow='\033[0;33m'
Blue='\e[34m'
BBlue='\e[44m'
FDefault='\e[49m'

LOGFILE="./overhead.log"
HOME_PATH="/home/aida"
BASE_PATH="${HOME_PATH}/k-bench"
CONFIG_PATH="config/default"

monitoring_wait=180
execute_count=720

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

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Installing now..."
    sudo apt-get update && sudo apt-get install -y jq
fi

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "vq is not installed. Installing now..."
    sudo snap install yq
fi

# Get to the directory
cd $BASE_PATH