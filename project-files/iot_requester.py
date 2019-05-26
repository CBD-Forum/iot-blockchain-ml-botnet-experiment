import sys
import time
import random
import schedule
import threading

import requests

from utils.helpers import address_list, random_headers

random.seed()


def make_request(ip):
    """Makes a request"""

    for n in range(random.randint(1, 3)):
        requests.get(ip, headers=random_headers())


def run_threaded(job_func, ip):
    """Run request in thread"""

    job_thread = threading.Thread(
        target=job_func,
        args=(ip,)
    )

    job_thread.start()


if __name__ == '__main__':
    args = sys.argv

    iot_num = int(args[1])
    address_block = args[2]

    ip_list = address_list(address_block)

    for ip in ip_list[:iot_num]:
        time.sleep(random.randint(3, 10))

        schedule.every(1).to(10).seconds.do(
            run_threaded, make_request, f'http://{ip}'
        )

    while 1:
        schedule.run_pending()
        time.sleep(1)
