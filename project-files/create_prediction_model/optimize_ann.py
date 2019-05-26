import logging

from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import RandomizedSearchCV

from config import ANN_OPTIMIZATION_PARAMETERS
from create_prediction_model.utils import log_runtime


logger = logging.getLogger('default')


def create_ann(optimizer='adam', activation='relu', dropout=0.2):
    """Returns ANN"""

    model = Sequential()

    model.add(
        Dense(
            units=38,
            kernel_initializer='uniform',
            activation=activation,
            input_dim=76
        )
    )

    model.add(Dropout(rate=dropout))

    model.add(
        Dense(units=38, kernel_initializer='uniform', activation=activation)
    )

    model.add(Dropout(rate=dropout))

    model.add(
        Dense(units=1, kernel_initializer='uniform', activation='sigmoid')
    )

    model.compile(
        optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy']
    )

    return model


@log_runtime()
def optimized_model_params(X_train=None, y_train=None):
    """
    Optimizes an ANN and returns the best hyperparameters for the final model
    """

    logger.debug(
        'Model optimization started, that will take long to complete...'
    )

    classifier = KerasClassifier(build_fn=create_ann)

    randomized_search = RandomizedSearchCV(
        estimator=classifier,
        param_distributions=ANN_OPTIMIZATION_PARAMETERS,
        n_iter=100,
        cv=10,
        n_jobs=-1,
        random_state=666,
        scoring='accuracy',
        return_train_score=True
    )

    randomized_search = randomized_search.fit(X_train, y_train)

    best_parameters = randomized_search.best_params_
    best_score = randomized_search.best_score_

    logger.info(f'Best score: {best_score} with parameters: {best_parameters}')

    means = randomized_search.cv_results_['mean_test_score']
    stds = randomized_search.cv_results_['std_test_score']
    params = randomized_search.cv_results_['params']

    for mean, stdev, param in zip(means, stds, params):
        logger.debug(
            f'Score: {mean} loss: {stdev} with parameters: {param}'
        )

    return best_parameters
