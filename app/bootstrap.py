import argparse
import logging
import logging.handlers
import logging.handlers
import os

import yaml

from app import BASE_DIR
from app.config import configuration, Configuration

CONFIG_FILE = os.path.join(BASE_DIR, "config.yml")


def load_yaml_config_file(yaml_config_file=CONFIG_FILE):
    if not os.path.exists(yaml_config_file):
        return {}
    with open(yaml_config_file, 'r') as ymlfile:
        result = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return result if result is not None else {}


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--configfile", help="where is the config file")

    args = parser.parse_args()

    if args.configfile is not None:
        yaml_config = load_yaml_config_file(args.configfile)
        configuration.update(**yaml_config)


def init_required_dirs(config: Configuration):
    """create the required dirs when the server is booting

    :param config:
    :return:
    """

    def foreach(callback, *iterables):
        for v in iterables:
            callback(v)

    def auto_makedir(v):
        if not os.path.exists(v):
            os.makedirs(v)

    target_dirs = [
        config.tmp_dir,
        config.log_dir,
    ]

    foreach(auto_makedir, *target_dirs)


def setup_logging(config: Configuration):
    def build_log_file_handler(logging_formatter, log_file_name):
        if config.log_rotating_type == 'time':
            log_file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(config.log_dir, log_file_name),
                                                                         when="D",
                                                                         backupCount=config.log_file_backups)
        else:
            log_file_handler = logging.handlers.RotatingFileHandler(os.path.join(config.log_dir, log_file_name),
                                                                    maxBytes=config.log_file_size,
                                                                    backupCount=config.log_file_backups)
        log_file_handler.setFormatter(logging_formatter)
        return log_file_handler

    logging_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s : %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging_formatter)

    root = logging.getLogger()
    root.addHandler(console_handler)
    root.addHandler(build_log_file_handler(logging_formatter, configuration.log_file))
    root.setLevel(config.log_level if config.log_level is not None else "INFO")


def bootstrap():
    """init configuration"""
    yaml_config = load_yaml_config_file()
    configuration.update(**yaml_config)
    process_args()
    configuration.validate()
    '''init path'''
    init_required_dirs(configuration)
    '''init log'''
    setup_logging(configuration)
