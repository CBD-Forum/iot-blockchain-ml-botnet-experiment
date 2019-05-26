import os
import glob
import time
import logging
import threading
import subprocess

from functools import partial, lru_cache
from multiprocessing import Pool

import docker
import schedule

from scapy.sendrecv import sniff
from scapy.utils import wrpcap

from detect_malicious_traffic import prepare_for_prediction, make_prediction
from utils.helpers import create_dir_if_not_exists

logger = logging.getLogger('default')

client = docker.from_env()


def convert_pcap_to_csv(processing_dir, output_dir):
    """Converts pcap files to csv flow file"""

    executable_dir = os.path.join(
        os.getenv('PROJECT_DIR'), 'CICFlowMeter-4.0', 'bin'
    )

    command = f'./cfm {processing_dir} {output_dir}'

    subprocess.call(command, shell=True, cwd=executable_dir)


def prepare_and_predict(processing_dir, csv_dir, output_dir, prediction_model):
    """Prepares csv data for prediction"""

    convert_pcap_to_csv(processing_dir, csv_dir)

    csv_files = [f for f in glob.glob(f'{csv_dir}/*.*.csv')]

    prepare_for_prediction_func = partial(
        prepare_for_prediction, output_dir
    )

    apply_action_in_list(prepare_for_prediction_func, csv_files)

    # Process and remove based on what csv_files list holds
    np_files = [
        os.path.join(output_dir,  f'{os.path.basename(f).split(".")[0]}.np')
        for f
        in csv_files
    ]

    make_prediction_func = partial(make_prediction, prediction_model)

    apply_action_in_list(make_prediction_func, np_files)

    pcap_files = [
        os.path.join(
            processing_dir,
            f'{os.path.basename(f).split(".")[0]}.pcap'
        )
        for f
        in csv_files
    ]

    clean_dir(pcap_files)

    clean_dir(csv_files)

    clean_dir(np_files)


def get_host_interface(docker_interface_prefix=None):
    """Get docker interface"""

    cmd = f"netstat -i | grep {docker_interface_prefix} | awk '{{ print $1 }}'"

    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    return stdout.decode().strip().split('\n')[0]


@lru_cache()
def get_container_ips_and_names(network=None, iot_prefix=None):
    """Returns container IPs in list"""

    containers_network_settings = [
        container
        for container
        in client.containers.list()
        if list(
            container.attrs['NetworkSettings']['Networks'].keys()
        )[0].startswith(network)
    ]

    return [
        (
            container.attrs['NetworkSettings']
            ['Networks'][network]['IPAddress'],
            container.name
        )
        for container
        in containers_network_settings
        if container.name.startswith(iot_prefix)
    ]


def capture_container_traffic(
        container_name, container_ip,
        host_interface, timeout, user, group, pcap_dir):
    """Tcpdump for each container"""

    capture_files_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        f'{pcap_dir}'
    )

    create_dir_if_not_exists(capture_files_dir, user, group)

    capture_file_name_path = os.path.join(
        capture_files_dir,
        f'{container_name}_{time.strftime("%Y%m%d-%H%M%S")}.pcap'
    )

    packets = sniff(
        iface=host_interface, filter=f'host {container_ip}', timeout=timeout
    )

    if len(packets):
        wrpcap(capture_file_name_path, packets)


def apply_action_in_list(func, list_arg, processes=4):
    """Helper function to apply actions in list element in parallel"""

    pool = Pool(processes)

    pool.map(func, list_arg)

    pool.close()

    pool.join()


def run_capture_container_traffic_threaded(
        job_func, c_name, c_ip, iface, timeout, whoami, grp, capture_dir):
    """Run capture_container_traffic threaded"""

    job_thread = threading.Thread(
        target=job_func,
        args=(c_name, c_ip, iface, timeout, whoami, grp, capture_dir)
    )

    job_thread.start()


def clean_dir(file_list):
    """Removes files in given list"""

    for file in file_list:
        if os.path.exists(file):
            os.remove(file)


if __name__ == "__main__":
    from config import (
        UID, GID, EXPERIMENT_NET, NETWORK_CAPTURE_CSV,
        SNIFF_TIMEOUT, NETWORK_CAPTURE, IOT_NAME_PREFIX,
        PREPARED_FOR_PREDICTION, PREDICTION_MODEL
    )

    create_dir_if_not_exists(NETWORK_CAPTURE_CSV, UID, GID)

    create_dir_if_not_exists(PREPARED_FOR_PREDICTION, UID, GID)

    docker_host_interface = get_host_interface(
        docker_interface_prefix=EXPERIMENT_NET
    )

    containers_ip_name = get_container_ips_and_names(
        network=EXPERIMENT_NET, iot_prefix=IOT_NAME_PREFIX
    )

    logger.info(
        f'Packet capture started for '
        f'docker host interface "{docker_host_interface}"'
    )

    for cnt_ip, cnt_name in containers_ip_name:
        schedule.every(SNIFF_TIMEOUT).seconds.do(
            run_capture_container_traffic_threaded,
            capture_container_traffic,
            cnt_name,
            cnt_ip,
            docker_host_interface,
            SNIFF_TIMEOUT,
            UID,
            GID,
            NETWORK_CAPTURE
        ).tag('network-watch')

    schedule.every(SNIFF_TIMEOUT / 4).seconds.do(
        prepare_and_predict,
        processing_dir=NETWORK_CAPTURE,
        csv_dir=NETWORK_CAPTURE_CSV,
        output_dir=PREPARED_FOR_PREDICTION,
        prediction_model=PREDICTION_MODEL
    ).tag('network-watch')

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        schedule.clear('network-watch')
