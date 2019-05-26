## An experimental setup to test ANN (artificial neural network) efficiency for detecting botnet attacks to IoT objects and recording the results to a blockchain

This repository contains the source code for my master's thesis.

#### System description
The experiment was developed on a MacBook Pro laptop with the following characteristics:  

|                       |                                                    |
| --------------------- | -------------------------------------------------- |
| Model Name            | MacBook Pro (Retina, 15-inch, Mid 2015)            |
| Processor Name        | Intel Core i7                                      |
| Processor Speed       | 2.5 GHz                                            |
| Number of Processors  | 1                                                  |
| Total Number of Cores | 4                                                  |
| L2 Cache (per Core)   | 256 KB                                             |
| L3 Cache              | 6 MB                                               |
| Memory                | 16 GB 1600 MHz DDR3                                |
| Graphics              | AMD Radeon R9 M370X 2048 MB Intel Iris Pro 1536 MB |

For this setup Vagrant is used to create an isolated, configurable and reproducible environment. 
Inside the virtual box, docker containers are used to simulate:  
&nbsp;&nbsp;&nbsp; a) the IoT objects  
&nbsp;&nbsp;&nbsp; b) the blockchain ([multichain](https://www.multichain.com/))  
&nbsp;&nbsp;&nbsp; c) the botnet ([mirai botnet](https://github.com/jgamblin/Mirai-Source-Code))  
The main programming language is python version 3.6.3.   

The experiment idea is that to initiate an attack from Mirai botnet to an IoT’s network.
Then, capture the IoT's network traffic, and with the help of an ANN (artificial neural network) analyse it. 
In case of successful malicious traffic detection, the incident will be recorded to a blockchain.
The blockchain -through a callback- will inform the system administrator -us- that potential malicious traffic is going through the IoT network.


#### Prerequisite software
Project setup requires [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).  

Follow the links to get the appropriate version for your platform.  
In order to run Vagrantfile properly, the following plugin needs to be installed first:

```shell
$ vagrant plugin install vagrant-host-shell
```

Then, clone the [experiment repo](https://github.com/anarchos78/iot-blockchain-ml-botnet-experiment). Open a terminal and:

```shell
$ git clone git@github.com:anarchos78/iot-blockchain-ml-botnet-experiment.git
```

#### Run the experiment
Spin up the virtual environment:

```shell
$ cd iot-blockchain-ml-botnet-experiment
$ vagrant up
```

Be patient, bootstrap takes a while.  
After vagrant completes the bootstrap process, attack instructions will be printed on screen similar to bellow:

```shell
Attack instructions:
1. ssh to the box => vagrant ssh
2. to connect to mirai botnet, issue to the terminal => telnet 192.168.0.5
3. then, enter mirai credentials (*Username* and *Password* is -root- for both)
4. to start an attack issue the command => syn 192.168.0.2,192.168.0.3,192.168.0.4 120
5. to list mirai attack types issue => ?
```
_* More details on mirai attack instructions [here](mirai-attack-instructions.md)_

_I suggest the use of a terminal multiplexer (tmux or screen).
Terminal multiplexer allows multiple terminal sessions to be accessed simultaneously in a single panel. Otherwise use multiple terminal windows._

Open 3 terminals. 
Login to the virtual box from all 3 terminals (`vagrant ssh`).  

- In the first terminal follow the aforementioned "Attack instructions" to initiate an attack.  

- In the second terminal issue the following command: `less -S +F  logs/iot-trust-level.log`. 
This command will "stream" the file contents on the screen as they are written in the file.  
Blockchain uses `iot-trust-level.log` file to log a possibly malicious traffic activity detected by the ANN, for administrator's consideration.  

- In the third terminal issue `less -S +F  logs/info.log`. Any IoT shutdown will be reported here, so, it's useful to keep an eye on it.

In the case of successful malicious traffic detection, a similar message to the one below will be logged in `iot-trust-level.log` file:
```shell
On 2019-01-01 00:00:01 "remote-thermometer-0" trust level was low. Please take action!
```

In the case of successful attack from mirai, a similar message to the one below will logged in `info.log` file:
```shell
2019-01-01 00:00:01,001 - detect_malicious_traffic.py - INFO - >>>>> IoT object "remote-thermometer-0" is down. TAKE ACTION <<<<<
```

Another way to see blockchain's records (essentially the "trust level" of each IoT object), is to query the blockchain's API via curl:

```shell
# Get the "trust_level" status of "remote-thermometer-0" IoT object
$ curl masternode:4444 \
-u user:PaSsWoRd \
-H "Content-Type: application/json" \
-d '{"method":"liststreamkeyitems","params":["trust_level","remote-thermometer-0",false,1]}' | python -m json.tool

# To decode HEX value to UTF-8
$ echo <put here the "data" value from the curl call> | xxd -p -r | python -m json.tool

# The output will be something like:
{
    "iot_id": "remote-thermometer-0",
    "trust_level": "high",
    "ts": "2019-01-01 00:00:01"
}
```



### Experiment parts

#### IoT objects
Each IoT object, simulates a remote thermometer which exposes a single URI to get the current temperature from the thermometer itself. 
For example, if you curl an IoT like `curl remote-thermometer-0` or `curl <IoT IP>`. The response will be:  
```shell
{
   "object": "remote-thermometer-0",
   "temperature": "3.66 Celsius"
}
```

_*Within the vagrant box you can find "hostname to IoT IP" mapping by looking into the hostsfile: `sudo cat /etc/hosts`._


#### Multichain
Apart from the IoT network, the experiment uses `multichain` as blockchain. 
More details about `multichain` at https://www.multichain.com/.    
Below is a list with basic `multichain` curl commands:

```shell
# To list streams
$ curl masternode:4444 \
-u user:PaSsWoRd \
-H "Content-Type: application/json" \
-d '{"method":"liststreams","params":[]}' | python -m json.tool

# To list stream publishers (in our cace from "trust_level" stream)
$ curl masternode:4444 \
-u user:PaSsWoRd \
-H "Content-Type: application/json" \
-d '{"method":"liststreampublishers","params":["trust_level"]}' | python -m json.tool

# To list the keys in a stream ("trust_level")
$ curl masternode:4444 \
-u user:PaSsWoRd \
-H "Content-Type: application/json" \
-d '{"method":"liststreamkeys","params":["trust_level"]}' | python -m json.tool
```

#### Mirai
The last part of the experiment objects is the `Mirai` botnet. 
For more details look at botnet [source](https://github.com/jgamblin/Mirai-Source-Code).


#### Experiment source
1. `CICFlowMeter-4.0`, it is used for network analysis, details at [CICFlowMeter](https://github.com/ISCX/CICFlowMeter) and [here](http://www.netflowmeter.ca/netflowmeter.html)
2. `create_prediction_model`, module for creating an AAN model using TensorFlow and Keras. The produced model is used for network analysis
3. `docker_files`, the directory holds docker related files to build the experiment containers
4. `logs`, this directory holds experiment's logs. Additionally, a file named `iot-trust-level.log` will be created.
Any malicious traffic detected by the AAN will be recorded in blockchain, and eventually the blockchain will log the incident (for system admin use) by "writing" in this file
5. `multichain_notification`, this module is used by the `multichain` blockchain. Specifically, is used to notify the system administrator for potential attacks
6. `tests`, self explanatory -unit tests
7. `utils`, this module contains useful helper functions
8. `config.py`, this module holds various settings for the experiment in whole
9. `create_docker_compose`, on vagrant start up, this module will create a `docker-compose.yml` file, that in turn will bring up the _"container"_ part of the experiment with the appropriate network configuration
10. `detect_malicious_trafic.py`, this module is responsible for preparing and analysing network traffic with the help of ANN
11. `iot_network_watcher.py`, which is responsible to capture and analyse the IoT network traffic (will run as a background task in intervals)
12. `iot_requester.py`, responsible to produce legitimate network traffic to IoTs (will run as a background task in intervals)
13. `requirements.txt`, list of the required by the experiment python packages
14. `start_experiment.sh`, this script is responsible for starting the experiment. Check below for instructions
15. `stop_experiment.sh`, this script stops and destroys the experiment




### Experiment customization
There are two ways to customize the experiment:
1. Customize the `Vagrantfile` before initial vagrant up
2. After spinning up the virtual environment, by providing the appropriate variables to `start_experiment.sh` script within the virtual box

In the first case, the most obvious change that you might want to do is to change the number of running IoTs.
The number of running IoTs is defined by the variable `IOT_OBJECTS` (line number 4).
Keep in mind that there is a limitation on the container number that can be spinned up, imposed by host machine CPU and RAM capacity.  
`RETRAIN_MODEL` variable defines (1 for "true", 0 for "false") whether to retrain the ANN on virtual environment start up.
It is to be observed that ANN retrain is time consuming process.

In the second case, while in the virtual box, you can destroy the experiment by `$ ./stop_experiment.sh` 
and re-build it by passing arguments for the experiment parts that you want to change like so:
```shell
env IOT_OBJECTS=1 env RETRAIN_MODEL=0 ./start_experiment.sh
```

Note that `start_experiment.sh` got default arguments for all the required script parameters, so, you can start the experiment with a clean slate:
```shell
$ ./start_experiment.sh
```

_*It's suggested to take a look at `Vagrantfile`, `start_experiment.sh` and `stop_experiment.sh` to understand the experiment's logic better_
 


### Notes on the ANN model
The experiment comes with two pre-trained models for malicious traffic detection. The ANN models are used for binary classification (is traffic malicious? yes/no).  
More details on binary classification look [here](https://en.wikipedia.org/wiki/Binary_classification).  
The experiment's malicious traffic detection approach, is premised on the assumption that for both models the training dataset should not contain any Mirai botnet traffic.
I want to test whether both ANNs can classify successfully unseen botnet traffic, in this case Mirai. 
The training dataset provided by [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/).
A description for the dataset can be found [here](https://www.unb.ca/cic/datasets/botnet.html).

For the ANN training CIC __training__ dataset has been used. 
First model characteristics:
```shell
Model acc: 88.38%,
Loss: 28.18%,
Training parameters:
{
   'batch_size': 128,
   'epochs': 512,
   'optimizer': 'rmsprop',
   'activation': 'relu',
   'dropout': 0.2
}
```

For the AAN training, CIC __testing__ dataset has been used.
Second model characteristics:
```shell
Model acc: 94.92%,
Loss: 20.37%,
Training parameters:
{
   'batch_size': 128,
   'epochs': 512,
   'optimizer': 'rmsprop',
   'activation': 'relu',
   'dropout': 0.2
}
```

Although the second model hasn't been used for IoT network analysis, it might be a good idea to do so.  
The reasons are:  
&nbsp;&nbsp;&nbsp; a) in the dataset, no Mirai botnet traffic included (the same applies for the fist model training as well).  
&nbsp;&nbsp;&nbsp; b) the testing dataset includes a wider variety of botnet traffic in comparison to CIC __training__ dataset.
I suspect that the wider botnet network variety in the ANN's training dataset favours more accurate traffic classification of unseen botnets. 



### Vagrant box control
To bring up the environment, from the project root where the `Vagrantfile` resides issue:
```shell
$ vagrant up
```

After changing the Vagrantfile, to rebuild the environment correctly do:
```shell
$ vagrant destroy -f && vagrant up
```

To destroy the box:
```shell
$ vagrant destroy -f
```

More details on vagrant [here](https://www.vagrantup.com/docs/)

_*Allow minimum 5GB RAM to box (controlled by `VIRTUALBOX_MEMORY` variable)_



### Improvements
- It seems that the experiment needs more powerful machine than the one that it was built on.
Sometimes restarting the experiment solves performance issues (call `stop_experiment.sh` and then `start_experiment.sh` within the virtual box).
That might be an indication for Vagrant setup improvement.
- ANN training uses [CICFlowMeter-4.0](http://www.netflowmeter.ca/netflowmeter.html) for generating bidirectional flows and for network traffic feature extraction.
A possible improvement might be a selection of a smaller set of flow features that was originally used for training.
Smaller feature set, results in a reduced training time and possibly in a more accurate traffic classification.
- Include a [MQTT](http://mqtt.org/) to make a more "real case" experiment.
- Dockerize a real IoT (thermometer sensor) firmware.
- Dockerize ANN and network traffic capture.
- Dockerize the malicious traffic detection functionality.
- Improve malicious traffic detection by including a mechanism for the ANN to self-adjust the prediction algorithm parameters based on traffic monitoring on top of IoT network.
- Initiate various botnet attacks.
