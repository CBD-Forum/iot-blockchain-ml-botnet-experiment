import sys
import subprocess

from unittest import mock

sys.modules['detect_malicious_traffic'] = mock.MagicMock()

from tests.test_files.containers import containers

from iot_network_watcher import (
    client, get_host_interface, get_container_ips_and_names,
    convert_pcap_to_csv, prepare_and_predict
)

NETWORK = 'experiment_net'


def test_convert_pcap_to_csv():
    """Tests convert_pcap_to_csv function"""

    with mock.patch.object(subprocess, 'Popen') as mocked_popen:
        mocked_popen.return_value.communicate.return_value = None

        convert_pcap_to_csv(processing_dir=None, output_dir=None)

        assert mocked_popen.called


def test_prepare_and_predict():
    """Tests prepare_and_predict function"""

    with mock.patch('iot_network_watcher.clean_dir') as mocked_clean_dir:
        prepare_and_predict(
            processing_dir=None,
            csv_dir=None,
            output_dir=None,
            prediction_model=None
        )

        assert mocked_clean_dir.call_count == 3


def test_get_host_interface():
    """Tests get_host_interface function"""

    with mock.patch.object(subprocess, 'Popen') as mocked_popen:
        mocked_popen.return_value.communicate.return_value = \
            b'experiment_net', None

        interface = get_host_interface(NETWORK)

        assert interface == 'experiment_net'


def test_get_container_ips_and_names():
    """Tests get_container_ips_and_names function"""

    client.containers.list = mock.Mock(return_value=containers)

    container_ips_and_names = get_container_ips_and_names(
        network=NETWORK, iot_prefix='remote-thermometer'
    )

    expected_result = [
        (
            c.attrs['NetworkSettings']['Networks'][NETWORK]['IPAddress'],
            c.name
        )
        for c
        in containers
    ]

    assert sorted(container_ips_and_names) == sorted(expected_result)


@mock.patch('iot_network_watcher.capture_container_traffic')
def test_capture_container_traffic(mocked_capture_container_traffic):
    """Tests capture_container_traffic function"""

    with mock.patch('utils.helpers.create_dir_if_not_exists') as mocked_func:
        mocked_func.side_effect = mock.MagicMock()

        mocked_func()
        mocked_capture_container_traffic()

        assert mocked_func.called
        assert mocked_capture_container_traffic.called
