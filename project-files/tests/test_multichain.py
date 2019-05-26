import unittest

from unittest import mock

from multichain_notification.multichain import BlockChainInterface


class TestMultichain(unittest.TestCase):
    """Test multichain"""

    def setUp(self):
        """Set Up"""

        self.tx_id = '1234567890'
        self.rpcuser = 'someone'
        self.rpcpasswd = 'some_password'
        self.rpchost = 'localhost'
        self.rpcport = '4444'
        self.chainname = 'iot_trust'
        self.stream_name = 'trust_level'
        self.log_file_name = 'iot_trust_level.log'

        self.client = BlockChainInterface(
            rpcuser=self.rpcuser,
            rpcpasswd=self.rpcpasswd,
            rpchost=self.rpchost,
            rpcport=self.rpcport,
            chainname=self.chainname,
            stream_name=self.stream_name,
            log_file_name=self.log_file_name
        )

        self.iot_id = "remote-thermometer-0"

        self.msg = {
            "iot_id": self.iot_id,
            "trust_level": "high",
            "ts": "2019-02-12 19:01:35"
        }

    def test_msg_to_hex(self):
        """Tests msg_to_hex method"""

        convert_msg_to_hex = self.client.msg_to_hex(self.msg)

        msg_in_hex = (
            '7b22696f745f6964223a202272656d6f74652d746865726d6f6d657465722'
            'd30222c202274727573745f6c6576656c223a202268696768222c20227473'
            '223a2022323031392d30322d31322031393a30313a3335227d'
        )

        self.assertEqual(convert_msg_to_hex, msg_in_hex)

    @mock.patch(
        'multichain_notification.multichain.BlockChainInterface.add_to_stream'
    )
    def test_add_to_stream(self, mock_add_to_stream):
        """Tests add_to_stream method"""

        mock_response = mock.Mock()

        expected_json = {
            "result": "1234567890",
            "error": None,
            "id": None
        }

        mock_response.json.return_value = expected_json
        mock_add_to_stream.return_value = mock_response

        response = self.client.add_to_stream(self.stream_name, self.iot_id)

        self.assertEqual(response.json(), expected_json)

    @mock.patch(
        'multichain_notification.multichain.BlockChainInterface.list_streams'
    )
    def test_list_streams(self, mock_list_streams):
        """Tests list_streams method"""

        mock_response = mock.Mock()

        expected_json = {
            "result": [
                {
                    "name": "root",
                    "createtxid": "2cdecce34632aa4",
                    "streamref": "0-0-0",
                    "open": True,
                    "details": {},
                    "subscribed": True,
                    "synchronized": True,
                    "items": 0,
                    "confirmed": 0,
                    "keys": 0,
                    "publishers": 0
                },
                {
                    "name": "trust_level",
                    "createtxid": "23d4c4386973fb6",
                    "streamref": "3-265-54307",
                    "open": True,
                    "details": {},
                    "subscribed": True,
                    "synchronized": True,
                    "items": 4,
                    "confirmed": 4,
                    "keys": 3,
                    "publishers": 1
                }
            ],
            "error": None,
            "id": None
        }

        mock_response.json.return_value = expected_json
        mock_list_streams.return_value = mock_response

        response = self.client.list_streams()

        self.assertEqual(response.json(), expected_json)

    @mock.patch(
        'multichain_notification.multichain.'
        'BlockChainInterface.list_stream_keys'
    )
    def test_list_streams_keys(self, mock_list_stream_keys):
        """Tests list_stream_keys method"""

        mock_response = mock.Mock()

        expected_json = {
            "result": [
                {
                    "key": "remote-thermometer-0",
                    "items": 2,
                    "confirmed": 2
                },
                {
                    "key": "remote-thermometer-1",
                    "items": 1,
                    "confirmed": 1
                },
                {
                    "key": "remote-thermometer-2",
                    "items": 1,
                    "confirmed": 1
                }
            ],
            "error": None,
            "id": None
        }

        mock_response.json.return_value = expected_json
        mock_list_stream_keys.return_value = mock_response

        response = self.client.list_stream_keys()

        self.assertEqual(response.json(), expected_json)

    @mock.patch(
        'multichain_notification.multichain.'
        'BlockChainInterface.list_stream_publishers'
    )
    def test_list_stream_publishers(self, mock_list_stream_publishers):
        """Tests list_stream_publishers method"""

        mock_response = mock.Mock()

        expected_json = {
            "result": [
                {
                    "publisher": "1DBBcLUZWnEteAgkF1j9SCda2Q8zmYpngqh8F3",
                    "items": 4,
                    "confirmed": 4
                }
            ],
            "error": None,
            "id": None
        }

        mock_response.json.return_value = expected_json
        mock_list_stream_publishers.return_value = mock_response

        response = self.client.list_stream_publishers()

        self.assertEqual(response.json(), expected_json)

    @mock.patch(
        'multichain_notification.multichain.'
        'BlockChainInterface.list_stream_key_items'
    )
    def test_list_stream_key_items(self, mock_list_stream_key_item):
        """Tests list_stream_key_items method"""

        mock_response = mock.Mock()

        expected_json = {
            "result": [
                {
                    "publisher": "1DBBcLUZWnEteAgkF1j9SCda2Q8zmYpngqh8F3",
                    "items": 4,
                    "confirmed": 4
                }
            ],
            "error": None,
            "id": None
        }

        mock_response.json.return_value = expected_json
        mock_list_stream_key_item.return_value = mock_response

        response = self.client.list_stream_key_items(stream_key='some_key')

        self.assertEqual(response.json(), expected_json)

    @mock.patch(
        'multichain_notification.multichain.'
        'BlockChainInterface.get_last_trust_level_data_by_tx_id'
    )
    def test_get_last_trust_level_data_by_tx_id(
            self, mock_get_last_trust_level_data_by_tx_id):
        """Tests get_last_trust_level_data_by_tx_id method"""

        mock_response = mock.Mock()

        expected_text = "high"

        mock_response.text = expected_text
        mock_get_last_trust_level_data_by_tx_id.return_value = mock_response

        response = self.client.get_last_trust_level_data_by_tx_id()

        self.assertEqual(response.text, "high")

    def _mocked_get_last_trust_level_data_by_tx_id(self):
        """Mocked get_last_trust_level_data_by_tx_id"""

        text = (
            'On {} "{}" trust level was {}. '
            'Please take action!\n'.format(
                self.msg['ts'], self.msg['iot_id'], "low"
            )
        )

        return text

    @mock.patch(
        'multichain_notification.multichain.'
        'BlockChainInterface.notify_low_trust_level'
    )
    def test_notify_low_trust_level(
            self, mock_notify_low_trust_level):
        """Tests notify_low_trust_level method"""

        self.client.get_last_trust_level_data_by_tx_id = \
            self._mocked_get_last_trust_level_data_by_tx_id()

        data = self.client.get_last_trust_level_data_by_tx_id

        self.client.notify_low_trust_level()

        self.assertTrue(mock_notify_low_trust_level.called)

        expected = (
            'On 2019-02-12 19:01:35 "remote-thermometer-0" '
            'trust level was low. Please take action!\n'
        )

        self.assertEqual(data, expected)
