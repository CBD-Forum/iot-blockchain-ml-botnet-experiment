import os
import sys
import time
import json
import binascii

from Savoir import Savoir


class BlockChainInterface(object):
    """Interfaces Multichain blockchain"""
    TRUST_LEVELS = {
        "low": binascii.b2a_hex(b"low").decode('utf-8'),
        "normal": binascii.b2a_hex(b"normal").decode('utf-8'),
        "high": binascii.b2a_hex(b"high").decode('utf-8')
    }

    def __init__(self,
                 tx_id=None,
                 rpcuser=os.getenv('RPC_USER'),
                 rpcpasswd=os.getenv('RPC_PASSWORD'),
                 rpchost=os.getenv('RPC_HOST'),
                 rpcport=os.getenv('RPC_PORT'),
                 chainname=os.getenv('CHAINNAME'),
                 stream_name=os.getenv('STREAM_NAME'),
                 log_file_name=os.getenv('LOW_TRUST_LEVEL_LOG_FILE')):
        """The constructor"""

        self.tx_id = tx_id
        self.rpcuser = rpcuser
        self.rpcpasswd = rpcpasswd
        self.rpchost = rpchost
        self.rpcport = rpcport
        self.chainname = chainname
        self.stream_name = stream_name
        self.log_file_name = log_file_name

        self.api = Savoir(
            self.rpcuser, self.rpcpasswd,
            self.rpchost, self.rpcport, self.chainname
        )

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.logdir = os.path.join(self.current_path, 'logs')
        self.logfile_path = os.path.join(
            self.current_path, 'logs', log_file_name
        )

    @staticmethod
    def msg_to_hex(msg):
        """Returns hexadecimal string"""
        return binascii.b2a_hex(json.dumps(msg).encode()).decode('utf-8')

    def add_to_stream(self, iot_id, trust_level):
        """
        Adds the trust level of IoT object
        :param iot_id: str
        :param trust_level: str, choice of "low", "high", "normal"
        :return:
        """

        data = {
            "iot_id": iot_id,
            "trust_level": trust_level,
            "ts": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        }

        self.api.publish(self.stream_name, iot_id, self.msg_to_hex(data))

    def list_streams(self):
        """Lists blockchain streams"""
        return self.api.liststreams(self.stream_name)

    def list_stream_keys(self):
        """Lists blockchain stream keys"""
        return self.api.liststreamkeys(self.stream_name)

    def list_stream_publishers(self):
        """Lists blockchain stream publishers"""
        return self.api.liststreampublishers(self.stream_name)

    def list_stream_key_items(self, stream_key=None, count=1):
        """Lists blockchain stream key items"""
        return self.api.liststreamkeyitems(
            self.stream_name, stream_key, False, count
        )

    def get_last_trust_level_data_by_tx_id(self):
        """Returns last published data of a given stream based on tx_id"""

        return bytearray.fromhex(
            self.api.getwallettransaction(self.tx_id)["data"][-1]
        ).decode()

    def notify_low_trust_level(self):
        """Logs low IoT "trust_level" from blockchain"""

        data = json.loads(self.get_last_trust_level_data_by_tx_id())

        iot_id = data["iot_id"]
        trust_level = data["trust_level"]
        ts = data["ts"]

        if trust_level == "low":
            text = (
                'On {} "{}" trust level was {}. '
                'Please take action!\n'.format(ts, iot_id, trust_level)
            )

            with open(self.logfile_path, 'a+') as f:
                os.chmod(self.logfile_path, 0o777)
                f.write(text)


if __name__ == "__main__":
    if len(sys.argv[1:]):
        tx_id = sys.argv[1]
        block_chain_interface = BlockChainInterface(tx_id=tx_id)
        block_chain_interface.notify_low_trust_level()
