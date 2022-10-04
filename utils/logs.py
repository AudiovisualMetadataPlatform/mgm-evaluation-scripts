import logging, sys

class Logs():
    def __init__(self):
        self.logger = logging.getLogger('mgm_evaluation')
        self.logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler('mgm_tests.log')
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                    '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        

    def error(self, msg):
        self.logger.error(logging.ERROR, msg)

    def info(self, msg):
        self.logger.log(logging.INFO, msg)