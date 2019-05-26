import os
import pwd
import logging.config

VAGRANT_USER = os.getenv('VAGRANT_USER', 'vagrant')

UID = pwd.getpwnam(VAGRANT_USER).pw_uid

GID = pwd.getpwnam(VAGRANT_USER).pw_gid

SNIFF_TIMEOUT = int(os.getenv('SNIFF_TIMEOUT', 60))

EXPERIMENT_NET = os.getenv('EXPERIMENT_NETWORK_NAME', 'experiment_net')

PREDICTION_MODEL = os.getenv('PREDICTION_MODEL', 'botnet_classifier.h5')

PROJECT_DIR = os.getenv('PROJECT_DIR', '/home/vagrant/code')

NETWORK_CAPTURE = os.getenv('IOT_PCAP_DIR')

NETWORK_CAPTURE_CSV = os.path.join(PROJECT_DIR, 'csv_flow_files')

PREPARED_FOR_PREDICTION = os.path.join(PROJECT_DIR, 'prepared_for_prediction')

IOT_NAME_PREFIX = os.getenv('IOT_NAME_PREFIX')

FIND_OPTIMUM_ANN_PARAMETERS = bool(
    int(os.getenv('FIND_OPTIMUM_ANN_PARAMETERS', False))
)

RETRAIN_MODEL = bool(int(os.getenv('RETRAIN_MODEL', False)))

ANN_OPTIMIZATION_PARAMETERS = {
    'batch_size': [32, 64, 128, 256, 512],
    'epochs': [256, 512],
    'optimizer': ['adam', 'rmsprop'],
    'activation': ['relu', 'linear'],
    'dropout': [0.2, 0.25, 0.3]
}

ANN_PARAMETERS = {
    'batch_size': 128,
    'epochs': 512,
    'optimizer': 'rmsprop',
    'activation': 'relu',
    'dropout': 0.2
}

LOG_DIR = os.path.join(PROJECT_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': (
                '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
            )
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },

        'iot_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': os.path.join(
                LOG_DIR,
                os.getenv('LOW_TRUST_LEVEL_LOG_FILE', 'iot-trust-level.log')
            ),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },

        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },

        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        }
    },

    'loggers': {
        'default': {
            'level': 'INFO',
            'handlers': ['info_file_handler'],
            'propagate': False
        }
    }
}

DATASET_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'create_prediction_model',
    'dataset'
)

DUMP_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'create_prediction_model',
    'dumps'
)

MODELS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'create_prediction_model',
    'models'
)

RAW_TRAINING_DATASET_PATH = os.path.join(
    DATASET_DIR, 'ISCX_Botnet-Training.pcap_ISCX.csv'
)

RAW_TESTING_DATASET_PATH = os.path.join(
    DATASET_DIR, 'ISCX_Botnet-Testing.pcap_ISCX.csv'
)

X_TRAIN_FILE_PATH = os.path.join(DUMP_DIR, 'X_train.np')

X_TEST_FILE_PATH = os.path.join(DUMP_DIR, 'X_test.np')

Y_TRAIN_FILE_PATH = os.path.join(DUMP_DIR, 'Y_train.np')

Y_TEST_FILE_PATH = os.path.join(DUMP_DIR, 'Y_test.np')

MALICIOUS_IPS = [
    '10.0.2.15',
    '10.37.130.4',
    '131.202.243.84',
    '147.32.84.130',
    '147.32.84.140',
    '147.32.84.150',
    '147.32.84.160',
    '147.32.84.170',
    '147.32.84.180',
    '158.65.110.24',
    '172.16.253.129',
    '172.16.253.130',
    '172.16.253.131',
    '172.16.253.132',
    '172.16.253.240',
    '172.29.0.109',
    '172.29.0.116',
    '192.168.1.103',
    '192.168.1.103',
    '192.168.1.105',
    '192.168.106.131',
    '192.168.106.141',
    '192.168.2.105',
    '192.168.2.109',
    '192.168.2.110',
    '192.168.2.110',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.112',
    '192.168.2.113',
    '192.168.2.113',
    '192.168.248.165',
    '192.168.3.25',
    '192.168.3.35',
    '192.168.3.65',
    '192.168.4.118',
    '192.168.4.118',
    '192.168.4.120',
    '192.168.4.120',
    '192.168.5.122',
    '192.168.5.122',
    '192.168.5.122',
    '192.168.5.122',
    '192.168.5.122',
    '192.168.5.122',
    '192.168.5.122',
    '198.164.30.2',
    '74.78.117.238'
]

logging.config.dictConfig(LOGGING)
