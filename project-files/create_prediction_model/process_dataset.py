import os
import math
import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from config import (
    RAW_TRAINING_DATASET_PATH, RAW_TESTING_DATASET_PATH,
    X_TRAIN_FILE_PATH, X_TEST_FILE_PATH,
    Y_TRAIN_FILE_PATH, Y_TEST_FILE_PATH, MALICIOUS_IPS
)
from create_prediction_model.utils import log_runtime

logger = logging.getLogger('default')


def read_dataset_from_csv(csv_path):
    """Returns the dataset from csv"""

    logger.debug(f'Reading data from "{csv_path}"')

    return pd.read_csv(csv_path, engine='python')


def normalize_row(row):
    """
    Convert values like Infinity, negative Infinity and NaN to numerical values
    """

    features = list()

    for i, value in enumerate(row):
        if float(value) == float("inf"):
            value = 10e5
        if math.isnan(float(value)):
            value = 0
        if float(value) == float("-inf"):
            value = -10e5

        features.append(float(value))

    return np.array(features, dtype=np.float32)


def load_data(raw_data, for_prediction=False):
    """Returns X [independent variables] ans Y [dependent variables]"""

    X = []
    Y = []

    logger.debug(
        f'The dataset has {raw_data.shape[1]} columns and {raw_data.shape[0]} '
        f'rows. Processing might take some time, be patient...'
    )

    sc = StandardScaler()

    for row in raw_data.values:
        np.delete(row, 61)

        ips = row[1], row[3]

        X.append(normalize_row(row[7:83]))

        if any(ip in ips for ip in MALICIOUS_IPS):
            Y.append(1)
        else:
            Y.append(0)

    logger.debug('Data has been loaded')

    if for_prediction:
        return np.array(sc.fit_transform(X), dtype=np.float32)

    return np.array(sc.fit_transform(X), dtype=np.float32), \
        np.array(Y, dtype=np.uint8)


def dump_to_disk(dump_file_path, data):
    """
    Save numpy objects to disk for later use
    """

    logger.debug(
        f'Saving object in file "{dump_file_path}", please wait...'
    )

    with open(dump_file_path, 'wb') as fh:
        np.save(fh, data)

    # Cleanup memory
    del data

    logger.debug(f'Saving completed')


@log_runtime()
def prepare_training_data():
    """Prepares the training data"""

    dump_file_paths = [
        X_TRAIN_FILE_PATH,
        X_TEST_FILE_PATH,
        Y_TRAIN_FILE_PATH,
        Y_TEST_FILE_PATH
    ]

    logger.debug('Data processing started, please wait...')

    # Check if training data already processed and load them from disk
    if all(os.path.exists(path) for path in dump_file_paths):
        logger.info('Data files already exist, proceed with model training')
    else:
        # Training data preparation
        raw_training_dataset = read_dataset_from_csv(RAW_TRAINING_DATASET_PATH)

        train_X, train_Y = load_data(raw_training_dataset)

        logger.info('Training dataset processed')

        dump_to_disk(X_TRAIN_FILE_PATH, np.array(train_X, dtype=np.float32))

        dump_to_disk(Y_TRAIN_FILE_PATH, np.array(train_Y, dtype=np.uint8))

        logger.info('Training features dumped')

        #######################################################################

        # Testing data preparation
        raw_testing_dataset = read_dataset_from_csv(RAW_TESTING_DATASET_PATH)

        test_X, test_Y = load_data(raw_testing_dataset)

        logger.info('Testing dataset processed')

        dump_to_disk(X_TEST_FILE_PATH, np.array(test_X, dtype=np.float32))

        dump_to_disk(Y_TEST_FILE_PATH, np.array(test_Y, dtype=np.uint8))

        logger.info('Testing features dumped')
