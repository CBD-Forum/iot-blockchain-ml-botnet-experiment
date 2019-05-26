import logging

from timeit import default_timer as timer

import numpy as np

from sklearn.model_selection import train_test_split


def load_data_from_file(file_path):
    """Returns numpy data from file"""

    with open(file_path, 'rb') as content:
        return np.load(content)


def split_dataset(X, Y, test_size=0.2):
    """Returns train and test subset from given dataset"""

    return train_test_split(
        X, Y, test_size=test_size, random_state=0
    )


def get_time(sec):
    """Returns a human friendly time representation of seconds"""
    day = sec // (24 * 3600)
    time = sec % (24 * 3600)
    hour = time // 3600

    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time

    return f'{int(day)} days, {int(hour)} hours, ' \
           f'{int(minutes)} minutes, {int(seconds)} seconds'


def log_runtime(level='info'):
    """Logs function runtime"""

    def decorator_log_runtime(func):
        def wrapper(*args, **kwargs):
            _log_level = {
                'CRITICAL': 50,
                'ERROR': 40,
                'WARNING': 30,
                'INFO': 20,
                'DEBUG': 10,
                'NOTSET': 0
            }

            logger = logging.getLogger('default')

            start = timer()

            result = func(*args, **kwargs)

            end = timer()
            time_elapsed = get_time(end - start)

            logger.log(
                level=_log_level[level.upper()],
                msg=(
                    f'Method/function `{func.__name__}` '
                    f'took {time_elapsed} to finish'
                )
            )
            return result

        return wrapper

    return decorator_log_runtime
