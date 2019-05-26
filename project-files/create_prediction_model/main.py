import os
import sys
import logging

sys.path.append(".")

import numpy as np
from keras.models import load_model
from sklearn.metrics import confusion_matrix

from config import (
    MODELS_DIR, X_TRAIN_FILE_PATH, Y_TRAIN_FILE_PATH, RETRAIN_MODEL,
    FIND_OPTIMUM_ANN_PARAMETERS, ANN_PARAMETERS, PREDICTION_MODEL
)
from create_prediction_model.final_model_training import final_ann
from create_prediction_model.optimize_ann import optimized_model_params
from create_prediction_model.process_dataset import prepare_training_data
from create_prediction_model.utils import (
    log_runtime, split_dataset, load_data_from_file
)

# Disable "Your CPU supports instructions that this
# TensorFlow binary was not compiled to use: AVX2 FMA" message
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)


logger = logging.getLogger('default')


@log_runtime()
def main():
    """Entry point"""

    prepare_training_data()

    X_iscx_train = load_data_from_file(X_TRAIN_FILE_PATH)
    y_iscx_train = load_data_from_file(Y_TRAIN_FILE_PATH)

    # TODO: should try with the test dataset
    # X_iscx_test = load_data_from_file(X_TEST_FILE_PATH)
    # y_iscx_test = load_data_from_file(Y_TEST_FILE_PATH)

    # Split the training dataset
    X_train, X_test, y_train, y_test = split_dataset(
        X_iscx_train, y_iscx_train
    )

    model = None
    model_filepath = os.path.join(MODELS_DIR, PREDICTION_MODEL)

    if RETRAIN_MODEL:
        logger.info('Model creation started...')

        if FIND_OPTIMUM_ANN_PARAMETERS:
            logger.info('Finding the best hyperparameters, please wait...')

            best_parameters = optimized_model_params(X_train, y_train)
        else:
            logger.info('Training model with fixed hyperparameters')
            best_parameters = ANN_PARAMETERS

        model = final_ann(X_train, y_train, **best_parameters)

        scores = model.evaluate(X_test, y_test, verbose=0)

        msg = (
            f'Model {model.metrics_names[1]}: {scores[1] * 100:.2f}%, '
            f'{model.metrics_names[0]}: {scores[0] * 100:.2f}% '
            f'with parameters: {best_parameters}'
        )

        logger.debug(msg)

        print(msg)

        logger.info('Model creation finished')
    elif os.path.exists(model_filepath):
        logger.debug('Model exists, loading model from disk')

        model = load_model(model_filepath)

    logger.info('Predicting the test dataset results')

    y_predict = model.predict(X_test)
    y_predict = (y_predict > 0.5)

    logger.info('Making the confusion matrix')

    cm = confusion_matrix(y_test, y_predict)

    logger.info(cm)

    print(cm)


if __name__ == "__main__":
    main()
