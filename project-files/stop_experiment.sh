#!/usr/bin/env bash

EXPERIMENT_NETWORK_NAME="${EXPERIMENT_NETWORK_NAME:-experiment_net}"
IOT_REQUESTER="${IOT_REQUESTER:-/home/vagrant/code/iot_requester.py}"
NETWORK_WATCHER_SCRIPT="${NETWORK_WATCHER_SCRIPT:-/home/vagrant/code/iot_network_watcher.py}"

kill_process() {
    pid=$1

    if [[ "" !=  "$pid" ]]; then
      echo "killing $pid"
      sudo -E kill -9 $pid
    fi
}

remove_docker_network() {
    EXPERIMENT_NETWORK_NAME="${1:-experiment_net}"

    experiment_network=`docker network ls --filter name="$EXPERIMENT_NETWORK_NAME" | grep "$EXPERIMENT_NETWORK_NAME" | awk '{{ print $2 }}'`

    if [[ "$experiment_network" ]]; then
        echo -e "\e[31mRemoving network $EXPERIMENT_NETWORK_NAME\e[0m"
        docker-compose down --remove-orphans
        docker network rm "$EXPERIMENT_NETWORK_NAME"
    fi
}

IOT_REQUESTER_PID=`ps -eaf | grep "$IOT_REQUESTER" | grep -v grep | awk '{print $2}'`

NETWORK_WATCHER_PID=`ps -eaf | grep "$NETWORK_WATCHER_SCRIPT" | grep -v grep | awk '{print $2}'`

# Kill the iot_requester process if exists to start clean
kill_process "$IOT_REQUESTER_PID"

# Kill the network_watcher process if exists to start clean
kill_process "$NETWORK_WATCHER_PID"

remove_docker_network "$EXPERIMENT_NETWORK_NAME"
