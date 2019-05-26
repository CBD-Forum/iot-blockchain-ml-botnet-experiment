import os
import io
import sys
import pwd
import grp
import yaml

from config import LOG_DIR
from utils.helpers import address_list, random_credential


class YamlFormatter(yaml.Dumper):
    """Custom YAML dumper"""

    def increase_indent(self, flow=False, indentless=False):
        return super(YamlFormatter, self).increase_indent(flow, False)


def create_multichain(
        image_dir, rpc_user, rpc_password, chain_name, rpc_port, network_port,
        stream_name, master_node_name, slave_node_number, log_file):
    """Creates the multichain dict object"""

    multichain = {
        'services': {}
    }

    slave_nodes = dict()

    masternode = {
        f'{master_node_name}': {
            'build': f'./{image_dir}/kunstmaan-master-multichain',
            'container_name': master_node_name,
            'environment': {
                'RPC_USER': f'{rpc_user}',
                'RPC_PASSWORD': f'{rpc_password}',
                'CHAINNAME': f'{chain_name}',
                'NETWORK_PORT': f'{network_port}',
                'RPC_PORT': f'{rpc_port}',
                'RPC_HOST': f'{master_node_name}',
                'STREAM_NAME': f'{stream_name}',
                'LOW_TRUST_LEVEL_LOG_FILE': f'{log_file}',
                'RPC_ALLOW_IP': '0.0.0.0/0.0.0.0',
                'PARAM_TARGET_BLOCK_SIZE': 'target-block-time|30',
                'PARAM_ANYONE_CAN_CONNECT': 'anyone-can-connect|true',
                'WALLET_NOTIFY_NEW': (
                    '/multichain_notification/'
                    'notify-blockchain-new-transaction.sh'
                )
            },
            'volumes': [
                './multichain_notification:/multichain_notification',
                './logs:/multichain_notification/logs'
            ]
        }
    }

    for i in range(slave_node_number):
        slave_node = {
            f'slavenode{i}': {
                'build': f'./{image_dir}/kunstmaan-node-multichain',
                'container_name': f'slavenode{i}',
                'expose': [
                    f'{network_port}',
                    f'{rpc_port}'
                ],
                'environment': {
                    'CHAINNAME': f'{chain_name}',
                    'NETWORK_PORT': f'{network_port}',
                    'RPC_PORT': f'{rpc_port}',
                    'RPC_USER': f'{rpc_user}',
                    'RPC_PASSWORD': f'{rpc_password}',
                    'STREAM_NAME': f'{stream_name}',
                    'RPC_ALLOW_IP': '0.0.0.0/0.0.0.0',
                    'MASTER_NODE': f'{master_node_name}'
                },
                'links': [
                    f'{master_node_name}'
                ],
                'depends_on': [
                    f'{master_node_name}'
                ]
            }
        }

        slave_nodes.update(slave_node)

    multichain['services'].update(masternode)
    multichain['services'].update(slave_nodes)

    return multichain


def create_iot_object(
        image_dir, iot_name_suffix, iot_network, iot_name_prefix=None,
        iot_ip=None, ssh_user=None, ssh_password=None,
        vulnerable_iot_objects=None):
    """Creates the iot dict object"""

    iot_name = f'{iot_name_prefix}-{iot_name_suffix}'

    iot_object = {
        iot_name: {
            'image': iot_name,
            'build': {
                'context': f'./{image_dir}/iot',
                'args': [
                    f'app_name={iot_name}',
                    f'ssh_user={ssh_user}',
                    f'ssh_password={ssh_password}',
                    f'vulnerable_iot_objects={vulnerable_iot_objects}'
                ]
            },
            'container_name': iot_name,
            'networks': {
                iot_network: {
                    'ipv4_address': iot_ip
                }
            }
        }
    }

    return iot_object


def create_iot_objects(
        image_dir=None, iot_num=None, iot_network=None, iot_name_prefix=None,
        ip_list_for_iot=None, weak_ssh_username=None, weak_ssh_password=None,
        vulnerable_iot_objects=None):
    """Creates the iot dict objects"""

    iot_objects = dict()
    vulnerable_iot_objects_log_file = os.path.join(
        LOG_DIR, 'vulnerable_iot_objects.txt'
    )

    if os.path.exists(vulnerable_iot_objects_log_file):
        os.remove(vulnerable_iot_objects_log_file)

    for app_num in range(iot_num):
        if app_num < vulnerable_iot_objects:
            ssh_user = weak_ssh_username
            ssh_password = weak_ssh_password

            vulnerable_iot_object = (
                f'"iot_name": "{iot_name_prefix}-{app_num}" ::: "ssh_user": '
                f'"{ssh_user}" ::: "ssh_password": "{ssh_password}" '
                f'--- telnet IP: {ip_list_for_iot[app_num]} ::: '
                f'telnet login: "root" ::: telnet password: "root"\n'
            )

            with open(vulnerable_iot_objects_log_file, 'a+') as f:
                os.chmod(vulnerable_iot_objects_log_file, 0o777)
                f.write(vulnerable_iot_object)
        else:
            ssh_user = 'root'
            ssh_password = random_credential()

        iot_object = create_iot_object(
            image_dir,
            app_num,
            iot_network,
            iot_name_prefix,
            iot_ip=ip_list_for_iot[app_num],
            ssh_user=ssh_user,
            ssh_password=ssh_password,
            vulnerable_iot_objects=vulnerable_iot_objects
        )

        iot_objects.update(iot_object)

    return iot_objects


def mirai_botnet(image_dir, ip_list_for_botnet, iot_network):
    """Creates the mirai botnet objects"""

    botnet = dict()

    cnc_object = {
        'cnc': {
            'container_name': 'cnc',
            'build': f'./{image_dir}/mirai/cnc',
            'expose': [
                '23'
            ],
            'networks': {
                iot_network: {
                    'ipv4_address': ip_list_for_botnet[0]
                }
            }
        }
    }

    bot_object = {
        'bot': {
            'build': f'./{image_dir}/mirai/bot',
            'container_name': 'bot',
            'networks': {
                iot_network: {
                    'ipv4_address': ip_list_for_botnet[1]
                }
            }
        }
    }

    botnet.update(cnc_object)
    botnet.update(bot_object)

    return botnet


def network(network_name):
    """Returns the docker network object"""

    return {
        'networks': {
            network_name: {
                'external': True
            }
        }
    }


if __name__ == '__main__':
    args = sys.argv

    image_dir = args[1]
    iot_num = int(args[2])
    rpc_user = args[3]
    rpc_password = args[4]
    chain_name = args[5]
    rpc_port = args[6]
    network_port = args[7]
    stream_name = args[8]
    iot_network = args[9]
    master_node_name = args[10]
    log_file = args[11]
    iot_name_prefix = args[12]
    address_block = args[13]
    vm_user_and_group = args[14]
    weak_ssh_username = args[15]
    weak_ssh_password = args[16]
    slave_node_number = int(args[17])

    docker_compose_file_name = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'docker-compose.yml'
    )

    if iot_num <= 20:
        vulnerable_iot_objects = round(iot_num * 0.3) + 1
    elif 21 <= iot_num <= 50:
        vulnerable_iot_objects = round(iot_num * 0.25) + 1
    elif 51 <= iot_num <= 80:
        vulnerable_iot_objects = round(iot_num * 0.23) + 1
    elif 81 <= iot_num <= 120:
        vulnerable_iot_objects = round(iot_num * 0.22) + 1
    else:
        vulnerable_iot_objects = round(iot_num * 0.20) + 1

    ip_list = address_list(address_block)
    ip_list_for_iot = ip_list[:iot_num]
    ip_list_for_botnet = ip_list[iot_num:]

    services = create_multichain(
        image_dir,
        rpc_user,
        rpc_password,
        chain_name,
        rpc_port,
        network_port,
        stream_name,
        master_node_name,
        slave_node_number,
        log_file
    )

    iot_objects = create_iot_objects(
        image_dir,
        iot_num,
        iot_network,
        iot_name_prefix,
        ip_list_for_iot,
        weak_ssh_username,
        weak_ssh_password,
        vulnerable_iot_objects
    )

    botnet = mirai_botnet(image_dir, ip_list_for_botnet, iot_network)

    services['services'].update(iot_objects)

    services['services'].update(botnet)

    with io.open(docker_compose_file_name, 'w', encoding='utf8') as fh:
        fh.write("version: '3'\n\n")

        content = yaml.dump(
            services,
            Dumper=YamlFormatter,
            default_flow_style=False,
            allow_unicode=True
        )

        fh.write(content.replace('\'"', '"').replace('"\'', '"'))

        network_object = yaml.dump(
            network(iot_network),
            Dumper=YamlFormatter,
            default_flow_style=False,
        )

        fh.write('\n')

        fh.write(network_object.replace('\'"', '"').replace('"\'', '"'))

    os.chown(
        docker_compose_file_name,
        pwd.getpwnam(vm_user_and_group)[2],
        grp.getgrnam(vm_user_and_group)[2]
    )
