import os
import string
import random
import ipaddress

from fake_useragent import UserAgent


def address_list(address):
    """Returns an IP list based on given address"""

    return [
        str(ip)
        for ip
        in ipaddress.IPv4Network(address)
    ][2:]


def random_credential(length=50):
    """Returns a random alphanumeric string"""

    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        )
        for _ in range(length)
    )


def random_headers():
    """Returns random headers to send with requests"""

    ua = UserAgent(
        fallback=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        )
    )

    return {
        'User-Agent': ua.random,
        'Accept': (
            'text/html,application/xhtml+xml,'
            'application/xml;q=0.9,image/webp,*/*;q=0.8'
        )
    }


def create_dir_if_not_exists(path, user, group):
    """Creates directory and changes its user and group"""

    if not os.path.exists(path):
        os.mkdir(path)
        os.chown(path, user, group)
