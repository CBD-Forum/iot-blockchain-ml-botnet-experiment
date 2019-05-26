import os
import pwd
import shutil
import getpass

from utils.helpers import (
    address_list, random_credential, random_headers, create_dir_if_not_exists
)


def test_address_list():
    """Tests address_list function"""

    ip_list = address_list('192.168.0.0/16')

    expected_in_ip_list = [
        '192.168.254.14',
        '192.168.252.105',
        '192.168.255.254'
    ]

    assert len(ip_list) == 65534
    assert set(expected_in_ip_list).issubset(ip_list)


def test_random_credential():
    """Tests random_credential function"""

    credential = random_credential()

    assert len(credential) == 50

    credential = random_credential(length=10)

    assert len(credential) == 10


def test_random_headers():
    """Tests random_headers function"""

    headers = random_headers()

    assert 'User-Agent' in headers.keys()

    headers = random_headers()

    assert isinstance(headers['User-Agent'], str)


def test_create_dir_if_not_exists():
    """Tests create_dir_if_not_exists function"""

    username = getpass.getuser()
    user = pwd.getpwnam(username)[2]
    group = pwd.getpwnam(username).pw_gid

    new_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_dir'
    )

    create_dir_if_not_exists(new_dir, user, group)

    assert os.path.exists(new_dir)

    shutil.rmtree(new_dir)
