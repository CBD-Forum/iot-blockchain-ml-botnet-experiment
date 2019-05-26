import os
import logging

import requests
import numpy as np
import pandas as pd
import tensorflow as tf

from keras.models import load_model

from create_prediction_model.process_dataset import (
    read_dataset_from_csv, load_data, dump_to_disk
)
from create_prediction_model.utils import load_data_from_file
from multichain_notification.multichain import BlockChainInterface
from config import (
    PREDICTION_MODEL, MODELS_DIR, EXPERIMENT_NET, IOT_NAME_PREFIX
)

logger = logging.getLogger('default')


def is_down(cnt_name):
    """Checks if iot object is down"""

    from iot_network_watcher import get_container_ips_and_names

    CONTAINER_IPS_NAMES = get_container_ips_and_names(
        network=EXPERIMENT_NET, iot_prefix=IOT_NAME_PREFIX
    )

    cnt_ip = [
        cnt[0]
        for cnt
        in CONTAINER_IPS_NAMES
        if cnt[1] == cnt_name
    ][0]

    response = requests.get(f'http://{cnt_ip}')

    return not (response.status_code == requests.codes.ok)


def make_prediction(
        prediction_model=PREDICTION_MODEL, dataset_file_to_predict=None):
    """Makes prediction bases on the trained model"""

    if not os.path.exists(dataset_file_to_predict):
        return

    iot_object = os.path.basename(dataset_file_to_predict).split('_')[0]

    with tf.Session(graph=tf.Graph()) as sess:
        model = load_model(os.path.join(MODELS_DIR, prediction_model))

        prediction = model.predict(
            load_data_from_file(dataset_file_to_predict)
        )
        prediction = (prediction > 0.5)

        t = []
        f = []

        for p in prediction:
            if p[0]:
                t.append(p[0])
                continue
            f.append(p[0])

        if len(t) > len(f):
            if (len(prediction) > 60 and len(f) == 0) or \
                    (len(f) > 0 and len(f) / len(t) >= 0.6):
                BlockChainInterface().add_to_stream(iot_object, "low")
                return
        else:
            if len(prediction) >= 100:
                BlockChainInterface().add_to_stream(iot_object, "low")
                return

        BlockChainInterface().add_to_stream(iot_object, "high")

        return


def prepare_for_prediction(output_dir, data_file_path, test=False):
    """Prepares data for prediction"""

    filename = os.path.basename(data_file_path).split(".")[0]

    iot_object_name = filename.split('_')[0]

    if not test:
        if not pd.read_csv(data_file_path, low_memory=False).shape[0]:
            return

        # There is no point to prepare the data for prediction if IoT is down
        if is_down(iot_object_name):
            logger.info(
                f'>>>>> IoT object "{iot_object_name}"'
                f' is down. TAKE ACTION <<<<<'
            )
            return

    raw_dataset = read_dataset_from_csv(data_file_path)

    featurized_data = load_data(raw_dataset, for_prediction=True)

    featurized_data_file_path = os.path.join(
        output_dir, f'{filename}.np'
    )

    dump_to_disk(
        featurized_data_file_path, np.array(featurized_data, dtype=np.float32)
    )

    return featurized_data_file_path
