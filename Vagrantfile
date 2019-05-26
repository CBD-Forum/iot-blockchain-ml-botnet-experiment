# -*- mode: ruby -*-
# vi: set ft=ruby :

IOT_OBJECTS = 30
SNIFF_TIMEOUT = 10
RETRAIN_MODEL = 0
FIND_OPTIMUM_ANN_PARAMETERS = 0
VULNERABLE_SSH_USERNAME = "root"
VULNERABLE_SSH_PASSWORD = "1234"

PYTHON_VERSION = "3.6.3"
VAGRANT_HOME_DIR = "/home/vagrant"
VAGRANT_SYNCED_DIR = "/srv/synced"
PROJECT_DIR = File.join(VAGRANT_HOME_DIR, "code")
IOT_PCAP_DIR = File.join(PROJECT_DIR, "iot_network_pcap")
NETWORK_WATCHER_SCRIPT = File.join(PROJECT_DIR, "iot_network_watcher.py")
IOT_REQUESTER = File.join(PROJECT_DIR, "iot_requester.py")
PREDICTION_MODEL = "botnet_classifier.h5"

RPC_USER = "user"
RPC_PASSWORD = "PaSsWoRd"
CHAINNAME = "iot_blockchain"
RPC_PORT = 4444
NETWORK_PORT = 6999
STREAM_NAME = "trust_level"
BLOCKCHAIN_MASTERNODE_NAME = "masternode"
SLAVE_NODE_NUMBER = (IOT_OBJECTS / 2) + 1
LOW_TRUST_LEVEL_LOG_FILE = "iot-trust-level.log"
LOW_TRUST_LEVEL_LOG_PATH = File.join(PROJECT_DIR, "multichain_notification", LOW_TRUST_LEVEL_LOG_FILE)

EXPERIMENT_NETWORK_NAME = "experiment_net"
IOT_NAME_PREFIX = "remote-thermometer"

DOCKER_FILES = "docker_files"
DOCKER_NETWORK_SUBNET = "192.168.0.0/16"
DOCKER_NETWORK_GATEWAY = "192.168.0.1"

VIRTUALBOX_CPUS = 4
VIRTUALBOX_MEMORY = 5632
VIRTUALBOX_NAME = "experiment_box"

VM_USER_AND_GROUP = "vagrant"


Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder "synced", VAGRANT_SYNCED_DIR, create: true

  # Copy project files in the synced directory
  config.vm.synced_folder "project-files", PROJECT_DIR, type: "rsync"

  # Configure the VM
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = VIRTUALBOX_MEMORY
    vb.cpus = VIRTUALBOX_CPUS
    vb.name = VIRTUALBOX_NAME
  end

  config.vm.provision "shell",
  run: "always",
  inline: <<-EOF
      # adds a line to a file if it is not already in the file
      addline () {
        if [ ! -f "$2" ]; then
          touch "$2"
        fi
        grep -q -F "$1" "$2" || echo "$1" >> $2
      }

      echo "\e[31mAdding user "#{VM_USER_AND_GROUP}" to sudo group\e[0m"
      sudo usermod -aG sudo #{VM_USER_AND_GROUP}

      # Environment variables to be used in the experiment
      export IOT_OBJECTS=#{IOT_OBJECTS}
      export RPC_USER=#{RPC_USER}
      export RPC_PASSWORD=#{RPC_PASSWORD}
      export CHAINNAME=#{CHAINNAME}
      export RPC_PORT=#{RPC_PORT}
      export STREAM_NAME=#{STREAM_NAME}
      export RPC_HOST=#{BLOCKCHAIN_MASTERNODE_NAME}
      export LOW_TRUST_LEVEL_LOG_FILE=#{LOW_TRUST_LEVEL_LOG_FILE}
      export LOW_TRUST_LEVEL_LOG_PATH=#{LOW_TRUST_LEVEL_LOG_PATH}
      export PROJECT_DIR=#{PROJECT_DIR}
      export SNIFF_TIMEOUT=#{SNIFF_TIMEOUT}
      export IOT_PCAP_DIR=#{IOT_PCAP_DIR}
      export PREDICTION_MODEL=#{PREDICTION_MODEL}
      export EXPERIMENT_NETWORK_NAME=#{EXPERIMENT_NETWORK_NAME}
      export IOT_NAME_PREFIX=#{IOT_NAME_PREFIX}
      export FIND_OPTIMUM_ANN_PARAMETERS=#{FIND_OPTIMUM_ANN_PARAMETERS}
      export RETRAIN_MODEL=#{RETRAIN_MODEL}

      # ...and make them available in the vagrant user's shell
      addline 'export IOT_OBJECTS="#{IOT_OBJECTS}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export RPC_USER="#{RPC_USER}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export RPC_PASSWORD="#{RPC_PASSWORD}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export CHAINNAME="#{CHAINNAME}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export RPC_PORT="#{RPC_PORT}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export STREAM_NAME="#{STREAM_NAME}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export RPC_HOST="#{BLOCKCHAIN_MASTERNODE_NAME}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export LOW_TRUST_LEVEL_LOG_FILE="#{LOW_TRUST_LEVEL_LOG_FILE}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export LOW_TRUST_LEVEL_LOG_PATH="#{LOW_TRUST_LEVEL_LOG_PATH}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export PROJECT_DIR="#{PROJECT_DIR}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export SNIFF_TIMEOUT="#{SNIFF_TIMEOUT}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export IOT_PCAP_DIR="#{IOT_PCAP_DIR}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export PREDICTION_MODEL="#{PREDICTION_MODEL}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export EXPERIMENT_NETWORK_NAME="#{EXPERIMENT_NETWORK_NAME}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export IOT_NAME_PREFIX="#{IOT_NAME_PREFIX}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export FIND_OPTIMUM_ANN_PARAMETERS="#{FIND_OPTIMUM_ANN_PARAMETERS}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'export RETRAIN_MODEL="#{RETRAIN_MODEL}"' '#{VAGRANT_HOME_DIR}/.iotbashrc'

      sudo apt-get update
      sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
          -o Dpkg::Options::="--force-confdef" \
          -o Dpkg::Options::="--force-confold"
      sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
          -o Dpkg::Options::="--force-confdef" \
          -o Dpkg::Options::="--force-confold" \
          git \
          libreadline-gplv2-dev \
          libncursesw5-dev \
          libssl-dev \
          libsqlite3-dev \
          tk-dev \
          libgdbm-dev \
          libc6-dev \
          libbz2-dev \
          libjpeg8-dev \
          libgcc1-dbg \
          libpcap-dev \
          python3-pip \
          htop

      echo "\e[31mInstalling Java 8\e[0m"
      sudo -E add-apt-repository -y ppa:openjdk-r/ppa
      sudo apt-get update
      sudo DEBIAN_FRONTEND=noninteractive apt-get -y install openjdk-8-jdk

      echo "\e[31mInstalling Docker\e[0m"
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt-get update
      sudo apt-cache policy docker-ce
      sudo DEBIAN_FRONTEND=noninteractive apt-get install docker-ce=18.03.0~ce-0~ubuntu -y
      sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose
      sudo groupadd docker
      sudo gpasswd -a #{VM_USER_AND_GROUP} docker
      sudo service docker restart

      # Go to code directory when login
      addline 'cd #{PROJECT_DIR}' '#{VAGRANT_HOME_DIR}/.bashrc'

      export PYENV_ROOT="#{VAGRANT_HOME_DIR}/.pyenv"
      export PATH="$PYENV_ROOT/bin:$PATH"

      echo "\e[31mInstalling pyenv\e[0m"
      curl -sSL https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

      # Make pyenv available in the vagrant user's shell for developer convenience
      addline 'export PATH="#{VAGRANT_HOME_DIR}/.pyenv/bin:$PATH"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'eval "$(pyenv init -)"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'eval "$(pyenv virtualenv-init -)"' '#{VAGRANT_HOME_DIR}/.iotbashrc'
      addline 'source #{VAGRANT_HOME_DIR}/.iotbashrc' '#{VAGRANT_HOME_DIR}/.bashrc'

      # Set the .bash_profile to load the .bashrc for login shells
      addline 'case "$-" in *i*) if [ -r ~/.bashrc ]; then . ~/.bashrc; fi;; esac' '#{VAGRANT_HOME_DIR}/.bash_profile'

      # Enable pyenv
      eval "$(pyenv init -)"

      if [ ! -d "#{VAGRANT_HOME_DIR}/.pyenv/versions/#{PYTHON_VERSION}" ]; then
          pyenv install #{PYTHON_VERSION}
      else
          echo "\e[31mSkipping python version (#{PYTHON_VERSION}) installation\e[0m"
      fi

      pyenv global #{PYTHON_VERSION}

      # Fix for sudo not using $PYTHONPATH
      echo 'Defaults env_keep += "PYTHONPATH"' | sudo tee -a /etc/sudoers

      echo "\e[31mUpgrading pip\e[0m"
      pip install --upgrade pip
      echo "\e[31mUpgrading setuptools\e[0m"
      pip install --upgrade setuptools
      echo "\e[31mInstall essential packages\e[0m"
      pip install -r #{PROJECT_DIR}/requirements.txt

      echo "\e[31mRun unit tests...\e[0m"
      find #{PROJECT_DIR} | grep -E "(__pycache__|None|\.DS_Store|\.pyc|\.pyo$)" | sudo xargs rm -rf
      py.test #{PROJECT_DIR}

      # Retrain the ANN
      if (( #{RETRAIN_MODEL} == 1 )); then
          echo "\e[31mRetraining the ANN, please be patient...\e[0m"
          python -m create_prediction_model.main
      fi

      cd #{PROJECT_DIR}

      # Make "start_experiment.sh" and "stop_experiment.sh" executable
      sudo chmod +x #{PROJECT_DIR}/start_experiment.sh
      sudo chmod +x #{PROJECT_DIR}/stop_experiment.sh

      # Start experiment
      env DOCKER_FILES=#{DOCKER_FILES} \
      env NETWORK_PORT=#{NETWORK_PORT} \
      env EXPERIMENT_NETWORK_NAME=#{EXPERIMENT_NETWORK_NAME} \
      env LOW_TRUST_LEVEL_LOG_FILE=#{LOW_TRUST_LEVEL_LOG_FILE} \
      env VM_USER_AND_GROUP=#{VM_USER_AND_GROUP} \
      env SLAVE_NODE_NUMBER=#{SLAVE_NODE_NUMBER} \
      env DOCKER_NETWORK_GATEWAY=#{DOCKER_NETWORK_GATEWAY} \
      env PROJECT_DIR=#{PROJECT_DIR} \
      env VULNERABLE_SSH_USERNAME=#{VULNERABLE_SSH_USERNAME} \
      env VULNERABLE_SSH_PASSWORD=#{VULNERABLE_SSH_PASSWORD} \
      env BLOCKCHAIN_MASTERNODE_NAME=#{BLOCKCHAIN_MASTERNODE_NAME} \
      env RPC_PORT=#{RPC_PORT} \
      env RPC_USER=#{RPC_USER} \
      env RPC_PASSWORD=#{RPC_PASSWORD} \
      env CHAINNAME=#{CHAINNAME} \
      env STREAM_NAME=#{STREAM_NAME} \
      env IOT_NAME_PREFIX=#{IOT_NAME_PREFIX} \
      env IOT_OBJECTS=#{IOT_OBJECTS} \
      env DOCKER_NETWORK_SUBNET=#{DOCKER_NETWORK_SUBNET} \
      env IOT_REQUESTER=#{IOT_REQUESTER} \
      env NETWORK_WATCHER_SCRIPT=#{NETWORK_WATCHER_SCRIPT} \
      bash #{PROJECT_DIR}/start_experiment.sh
  EOF

end
