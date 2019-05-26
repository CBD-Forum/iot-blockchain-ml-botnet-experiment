import os

from config import LOG_DIR
from create_docker_compose import (
    create_multichain, create_iot_object, create_iot_objects, address_list,
    mirai_botnet, network
)


image_dir = "docker_local_images"
iot_num = 5
rpc_user = "user"
rpc_password = "pasword"
chain_name = "iot_blockchain"
rpc_port = 4444
network_port = 6999
stream_name = "trust_level"
iot_network = "experiment_net"
master_node_name = "masternode"
log_file = "log_file"
iot_name_prefix = "remote-thermometer"
address_block = "192.168.0.0/16"
vm_user_and_group = "vagrant"
weak_ssh_username = "root"
weak_ssh_password = 1234
slave_node_number = 2
ip_list = address_list(address_block)
ip_list_for_iot = ip_list[:iot_num]
ip_list_for_botnet = ip_list[iot_num:]


def test_create_multichain():
    """Tests create_multichain function"""

    multichain = create_multichain(
        image_dir=image_dir, rpc_user=rpc_user, rpc_password=rpc_password,
        chain_name=chain_name, rpc_port=rpc_port, network_port=network_port,
        stream_name=stream_name, master_node_name=master_node_name,
        slave_node_number=slave_node_number, log_file=log_file
    )

    assert 'services' in multichain.keys()
    assert 'slavenode0' in multichain['services'].keys()
    assert 'slavenode1' in multichain['services'].keys()


def test_create_iot_object():
    """Tests create_iot_object function"""

    iot = create_iot_object(
        image_dir=image_dir, iot_name_suffix=0, iot_network=iot_network,
        iot_name_prefix=iot_name_prefix, iot_ip='192.168.0.3',
        ssh_user=weak_ssh_username, ssh_password=weak_ssh_password,
        vulnerable_iot_objects=1
    )

    expected = {
      'remote-thermometer-0': {
        'image': 'remote-thermometer-0',
        'build': {
          'context': './docker_local_images/iot',
          'args': [
            'app_name=remote-thermometer-0',
            'ssh_user=root',
            'ssh_password=1234',
            'vulnerable_iot_objects=1'
          ]
        },
        'container_name': 'remote-thermometer-0',
        'networks': {
          'experiment_net': {
            'ipv4_address': '192.168.0.3'
          }
        }
      }
    }

    assert iot == expected


def test_create_iot_objects():
    """Tests create_iot_objects function"""

    _iots = create_iot_objects(
        image_dir=image_dir, iot_num=3, iot_network=iot_network,
        iot_name_prefix=iot_name_prefix, ip_list_for_iot=ip_list_for_iot,
        weak_ssh_username=weak_ssh_password,
        weak_ssh_password=weak_ssh_password,
        vulnerable_iot_objects=2
    )

    iots = _iots.keys()

    vulnerable_iot_objects_log_file = os.path.join(
        LOG_DIR, 'vulnerable_iot_objects.txt'
    )

    assert 'remote-thermometer-0' in iots
    assert 'remote-thermometer-1' in iots
    assert 'remote-thermometer-2' in iots
    assert 'remote-thermometer-3' not in iots
    assert os.path.exists(vulnerable_iot_objects_log_file)

    os.remove(vulnerable_iot_objects_log_file)


def test_mirai_botnet():
    """Tests mirai_botnet function"""

    _botnet = mirai_botnet(image_dir, ip_list_for_botnet, iot_network)

    botnet = _botnet.keys()

    assert 'cnc' in botnet
    assert 'bot' in botnet


def test_network():
    """Tests network function"""

    net = network(iot_network)

    assert 'networks' in net.keys()
    assert 'experiment_net' in net['networks'].keys()
