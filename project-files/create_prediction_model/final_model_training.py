import os
import logging

from config import MODELS_DIR
from create_prediction_model.optimize_ann import create_ann
from create_prediction_model.utils import log_runtime

logger = logging.getLogger('default')


@log_runtime()
def final_ann(X_train=None, y_train=None, **best_parameters):

    model = create_ann(
        optimizer=best_parameters['optimizer'],
        activation=best_parameters['activation'],
        dropout=best_parameters['dropout']
    )

    logger.info('Model training started, that might take long, please wait...')

    model.fit(
        X_train,
        y_train,
        batch_size=best_parameters['batch_size'],
        epochs=best_parameters['epochs'],
        validation_split=0.33
    )

    logger.info('Final model training finished')

    model_filepath = os.path.join(MODELS_DIR, 'botnet_classifier.h5')

    model.save(filepath=model_filepath)

    logger.debug(f'Model saved at: {model_filepath}')

    return model
