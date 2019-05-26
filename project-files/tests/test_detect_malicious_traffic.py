import os
import unittest

from unittest import mock

from detect_malicious_traffic import (
    make_prediction, prepare_for_prediction, is_down
)

TEST_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test_files'
)


class TestMakePredictionWrapper(unittest.TestCase):
    """Test case for make_prediction function"""

    @mock.patch(
        'multichain_notification.multichain.BlockChainInterface.add_to_stream'
    )
    def test_make_prediction(self, mock_add_to_stream):
        """Tests make_prediction function"""

        mock_add_to_stream.side_effect = None

        dataset_file_to_predict = os.path.join(
            TEST_DIR,
            'remote-thermometer-15_20190305-200357.np'
        )

        # In the try block we're expecting "TypeError"
        # in the case that "add_to_stream" method has been called
        # within make_prediction() function
        # before "BlockChainInterface" get initialized
        # with the proper arguments (when test run on "vagrant up").
        # The except block will reached only when "BlockChainInterface"
        # has been initialized with proper arguments
        # (when test run within the box - "add_to_stream" mocked successfully)
        try:
            with self.assertRaises(TypeError):
                make_prediction(
                    dataset_file_to_predict=dataset_file_to_predict
                )
        except Exception as e:
            self.assertTrue(mock_add_to_stream.called)
            self.assertEqual(mock_add_to_stream.call_count, 1)


def test_prepare_for_prediction():
    """Tests prepare_for_prediction function"""

    data_file_path = os.path.join(
        TEST_DIR,
        'remote-thermometer-0_20190309-105711.pcap_Flow.csv'
    )

    np_file = os.path.join(
        TEST_DIR,
        'remote-thermometer-0_20190309-105711.np'
    )

    prepare_for_prediction(TEST_DIR, data_file_path, test=True)

    assert os.path.exists(np_file)

    os.remove(np_file)


@mock.patch('requests.get')
def test_is_down(mocked_get):
    """Tests is_down function"""

    cnt_name_ip = [
        ('192.168.0.2', 'remote-thermometer-0'),
        ('192.168.0.3', 'remote-thermometer-1'),
        ('192.168.0.4', 'remote-thermometer-2')
    ]

    mocked_get.return_value.ok = False

    with mock.patch(
            'iot_network_watcher.get_container_ips_and_names') as mocked_func:
        mocked_func.return_value = cnt_name_ip

        iot_alive = is_down('remote-thermometer-0')

        assert iot_alive
