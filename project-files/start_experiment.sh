#!/usr/bin/env bash

DOCKER_FILES="${DOCKER_FILES:-docker_files}"
NETWORK_PORT="${NETWORK_PORT:-6999}"
EXPERIMENT_NETWORK_NAME="${EXPERIMENT_NETWORK_NAME:-experiment_net}"
LOW_TRUST_LEVEL_LOG_FILE="${LOW_TRUST_LEVEL_LOG_FILE:-iot-trust-level.log}"
VM_USER_AND_GROUP="${VM_USER_AND_GROUP:-vagrant}"
SLAVE_NODE_NUMBER="${SLAVE_NODE_NUMBER:-$((IOT_OBJECTS / 2 + 1))}"
DOCKER_NETWORK_GATEWAY="${DOCKER_NETWORK_GATEWAY:-192.168.0.1}"
PROJECT_DIR="${PROJECT_DIR:-/home/vagrant/code}"
VULNERABLE_SSH_USERNAME="${VULNERABLE_SSH_USERNAME:-root}"
VULNERABLE_SSH_PASSWORD="${VULNERABLE_SSH_PASSWORD:-1234}"
BLOCKCHAIN_MASTERNODE_NAME="${BLOCKCHAIN_MASTERNODE_NAME:-masternode}"
RPC_PORT="${RPC_PORT:-4444}"
RPC_USER="${RPC_USER:-user}"
RPC_PASSWORD="${RPC_PASSWORD:-PaSsWoRd}"
CHAINNAME="${CHAINNAME:-iot_blockchain}"
STREAM_NAME="${STREAM_NAME:-trust_level}"
IOT_NAME_PREFIX="${IOT_NAME_PREFIX:-remote-thermometer}"
IOT_OBJECTS="${IOT_OBJECTS:-30}"
DOCKER_NETWORK_SUBNET="${DOCKER_NETWORK_SUBNET:-192.168.0.0/16}"
IOT_REQUESTER="${IOT_REQUESTER:-/home/vagrant/code/iot_requester.py}"
NETWORK_WATCHER_SCRIPT="${NETWORK_WATCHER_SCRIPT:-/home/vagrant/code/iot_network_watcher.py}"

# Converts the message to be stored to the blockchain into hexadecimal
hex() {
    msg='{"iot_id":"'"$1"'","trust_level":"'"$2"'","ts":"'"`date '+%Y-%m-%d %H:%M:%S'`"'"}'
    printf '%s' "$msg"| xxd -p -u | tr -d '\n'
}

source "$PROJECT_DIR/stop_experiment.sh"

add_host() {
    ip=$1
    hostname=$2

    grep -q "'^$ip'" /etc/hosts && \
    sudo sed -i "'s/^$ip.*/$ip $hostname/'" /etc/hosts \
    || printf "%s %s\n" "$ip" "$hostname" | sudo tee -a /etc/hosts > /dev/null
}

if [ -f "$PROJECT_DIR/docker-compose.yml" ]; then
    echo -e "\e[31mRemoving $PROJECT_DIR/docker-compose.yml\e[0m"
    rm -rf "$PROJECT_DIR/docker-compose.yml"
fi

echo -e "\e[31mCreating $PROJECT_DIR/docker-compose.yml\e[0m"
sudo -E $(which python) "$PROJECT_DIR/create_docker_compose.py" \
    "$DOCKER_FILES" \
    "$IOT_OBJECTS" \
    "$RPC_USER" \
    "$RPC_PASSWORD" \
    "$CHAINNAME" \
    "$RPC_PORT" \
    "$NETWORK_PORT" \
    "$STREAM_NAME" \
    "$EXPERIMENT_NETWORK_NAME" \
    "$BLOCKCHAIN_MASTERNODE_NAME" \
    "$LOW_TRUST_LEVEL_LOG_FILE" \
    "$IOT_NAME_PREFIX" \
    "$DOCKER_NETWORK_SUBNET" \
    "$VM_USER_AND_GROUP" \
    "$VULNERABLE_SSH_USERNAME" \
    "$VULNERABLE_SSH_PASSWORD" \
    "$SLAVE_NODE_NUMBER"

experiment_network=`docker network ls --filter name="$EXPERIMENT_NETWORK_NAME" | grep "$EXPERIMENT_NETWORK_NAME" | awk '{{ print $2 }}'`

remove_docker_network "$experiment_network"

echo -e "\e[31mCreating network $EXPERIMENT_NETWORK_NAME\e[0m"
docker network create \
    --gateway "$DOCKER_NETWORK_GATEWAY" \
    --subnet "$DOCKER_NETWORK_SUBNET" \
    --opt com.docker.network.bridge.name="$EXPERIMENT_NETWORK_NAME" \
    --opt com.docker.network.bridge.enable_icc=true \
    "$EXPERIMENT_NETWORK_NAME"

echo -e "\e[31mBuilding the experiment\e[0m"
docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d

# Replace DEFAULT_JVM_OPTS for CICFlowMeter-4.0
sed -i 's#path=../#path=/home/vagrant/code/CICFlowMeter-4.0/#' /home/vagrant/code/CICFlowMeter-4.0/bin/cfm

masternode_ip=`docker inspect \
    -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
    "$BLOCKCHAIN_MASTERNODE_NAME"`

# add hostfile entry for the masternode
if ! grep -q "$BLOCKCHAIN_MASTERNODE_NAME" /etc/hosts; then
    add_host "$masternode_ip" "$BLOCKCHAIN_MASTERNODE_NAME"
fi

curl "$BLOCKCHAIN_MASTERNODE_NAME":"$RPC_PORT" \
    -u "$RPC_USER":"$RPC_PASSWORD" \
    -v -H "Content-Type: application/json" \
    -d '{"chain_name":"'$CHAINNAME'","version":"1.1","method":"create","params":["stream","'$STREAM_NAME'",true]}'

echo -e "\e[31m\nStream \"$STREAM_NAME\" created\n\e[0m"

# Subscribe to blockchain stream
echo -e "\e[31mSubscribe to \"$STREAM_NAME\" blockchain stream\n\e[0m"
curl "$BLOCKCHAIN_MASTERNODE_NAME":"$RPC_PORT" \
    -u "$RPC_USER":"$RPC_PASSWORD" \
    -H "Content-Type: application/json" \
    -d '{"chain_name":"'$CHAINNAME'","version":"1.1","method":"subscribe","params":["'$STREAM_NAME'"]}'

for i in $( seq 0 $((IOT_OBJECTS - 1)) );
do
  # Publish to stream the initial IoT trust level of "high"
  data=`hex "$IOT_NAME_PREFIX-${i}" "high"`

  curl "$BLOCKCHAIN_MASTERNODE_NAME":"$RPC_PORT" \
  -u "$RPC_USER":"$RPC_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"chain_name":"'$CHAINNAME'","version":"1.1","method":"publish","params":["'$STREAM_NAME'","'$IOT_NAME_PREFIX'-'${i}'","'"$data"'"]}'

  # fetch container IP
  container_ip=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$IOT_NAME_PREFIX"-${i}`

  # add hostfile entry for each IoT container
  if ! grep -q "$IOT_NAME_PREFIX"-${i} /etc/hosts; then
    add_host "$container_ip" "$IOT_NAME_PREFIX"-${i}
  fi
done

IOT_REQUESTER_PID=`ps -eaf | grep "$IOT_REQUESTER" | grep -v grep | awk '{print $2}'`

NETWORK_WATCHER_PID=`ps -eaf | grep "$NETWORK_WATCHER_SCRIPT" | grep -v grep | awk '{print $2}'`

# Kill the iot_requester process if exists to start clean
kill_process "$IOT_REQUESTER_PID"

# Kill the network_watcher process if exists to start clean
kill_process "$NETWORK_WATCHER_PID"

echo -e "\e[31m\nCleanup any leftovers\e[0m"
rm -rf iot_network_pcap/*.pcap \
&& rm -rf csv_flow_files/*.*.csv \
&& rm -rf prepared_for_prediction/*.np \
&& rm -rf logs/info.log \
&& rm -rf logs/iot-trust-level.log

echo -e "\e[31m\nRun the IoT requester to produce some legit traffic\e[0m"
nohup python "$IOT_REQUESTER" \
    "$IOT_OBJECTS" \
    "$DOCKER_NETWORK_SUBNET" </dev/null &>/dev/null &

echo -e "\e[31m\nStart capturing packets from the IoTs\e[0m"
sudo -E nohup $(which python) "$NETWORK_WATCHER_SCRIPT" </dev/null &>/dev/null &

cnc_ip=`sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cnc`
ips_to_attack=`python -c 'from utils.helpers import address_list; print(",".join(address_list("'$DOCKER_NETWORK_SUBNET'")[:int("'$IOT_OBJECTS'")]))'`
attack_cmd="syn $ips_to_attack 120"

red="\e[1;31m"
red_end="\e[0m"

instructions=$(cat <<EOF

$(echo -e "${red}Attack instructions:${red_end}")
$(echo -e "${red}1. ssh to the box => vagrant ssh${red_end}")
$(echo -e "${red}2. to connect to mirai botnet, issue to the terminal => telnet $cnc_ip${red_end}")
$(echo -e "${red}3. then, enter mirai credentials (*Username* and *Password* is -root- for both)${red_end}")
$(echo -e "${red}4. to start an attack issue the command => $attack_cmd${red_end}")
$(echo -e "${red}5. to list mirai attack types issue => ?${red_end}")
EOF
)

echo "$instructions"
