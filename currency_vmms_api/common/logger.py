import os
import sys
import logging

from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, config, name, file_name):
        self.log = self.__get_logger(config=config, name=name, file_name=file_name)

    @staticmethod
    def __get_logger(config, name, file_name, level=logging.WARNING):
        logger = logging.getLogger(name=name)

        if len(logger.handlers) > 1:
            return logger

        logger.setLevel(level)
        logger.addHandler(logging.StreamHandler(sys.stdout))

        if not os.path.exists(config.LOGS_FOLDER):
            os.mkdir(config.LOGS_FOLDER)

        log_file_name = os.path.join(config.LOGS_FOLDER, file_name)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = TimedRotatingFileHandler(
            log_file_name,
            when="midnight",
            interval=1,
            encoding="UTF-8",
            backupCount=365
        )
        file_handler.suffix = "%Y%m%d"
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
