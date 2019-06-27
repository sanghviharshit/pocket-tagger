import logging

class Log:
    @classmethod
    def get_logger(cls, name):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)
