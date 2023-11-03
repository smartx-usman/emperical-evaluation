#!/bin/bash

# include configurator script
source ./configurator.sh

result_file="result.txt"
coap_server="single"
coap_port="31839" # or 5683

rm -rf $result_file

pip3 install CoAPthon3

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
