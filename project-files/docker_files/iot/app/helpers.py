import os
import pickle

from datetime import datetime
from random import randint

import requests


def dummy_temperature(month, hour):
    """
    Returns a temperature for given month and hour
    based on UK weather statistics
    """

    temperature_range = {
        1: (1.2, 6.4),
        2: (0.9, 6.6),
        3: (2.0, 9.1),
        4: (3.9, 11.8),
        5: (6.8, 15.6),
        6: (9.7, 18.6),
        7: (11.7, 20.4),
        8: (11.5, 20.1),
        9: (9.6, 17.5),
        10: (7.2, 14.0),
        11: (3.6, 9.4),
        12: (2.0, 7.3)
    }

    low, high = temperature_range[month]

    increment = round((high - low) / 11, 2)

    temperatures_until_noon = []

    for i in range(1, 13):
        if not temperatures_until_noon:
            temperatures_until_noon.append(low)
        else:
            temperatures_until_noon.append(
                round(temperatures_until_noon[-1] + increment, 2)
            )

        if temperatures_until_noon[-1] > high:
            del temperatures_until_noon[-1]
            temperatures_until_noon.append(high)

    temperatures_until_noon.extend(temperatures_until_noon[::-1])

    return round(temperatures_until_noon[hour - 1] - randint(0, 99) / 100, 2)


def get_temperature():
    """Returns dummy temperature"""

    now = datetime.now()
    month = now.month
    hour = now.hour

    storage = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'temperature.pk'
    )

    if os.path.exists(storage):
        with open(storage, 'rb') as f:
            temperature_at_time = pickle.load(f)

        [(timestamp, temperature)] = temperature_at_time.items()

        date_from_file = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

        if hour > date_from_file.hour:
            os.remove(storage)

            temperature = dummy_temperature(month, hour)
            temperature_at_time = {date_from_file.hour: temperature}

            with open(storage, 'wb') as f:
                pickle.dump(temperature_at_time, f)
    else:
        with open(storage, 'wb') as f:
            temperature = dummy_temperature(month, hour)
            temperature_at_time = {f'{datetime.now()}': temperature}
            pickle.dump(temperature_at_time, f)

    return temperature


def send_temperature(temperature):
    """
    Mocks MQTT functionality by sending thermometer's output to an echo server
    """

    requests.get(url=f'http://httpbin.org/get?temperature={temperature}')

    return
