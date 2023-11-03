import datetime as dt
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
import environ

env = environ.Env()


from log4mongo.handlers import MongoHandler


class MongoFormatter(logging.Formatter):
    """Defines the log entry structure to be stored on the collection.

    Adapted from MongoFormatter of log4mongo. Removed some parameters
    and changed timestamp to local instead of UTC."""

    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""

        # Standard document
        document = {
            'timestamp': dt.datetime.now(),
            'level': record.levelname,
            'message': record.getMessage(),
            'loggerName': record.name
        }

        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })

        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]

        return document


class StdoutFormatter(logging.Formatter):

    RED = '\u001b[31m'
    YELLOW = '\u001b[33m'
    GREEN = '\u001b[32m'
    BLUE = '\u001b[34m'
    RST = '\u001b[0m'

    LOG_LEVELS = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED
    }

    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record: 'logging.LogRecord') -> str:
        fmt = StdoutFormatter.LOG_LEVELS[record.levelno] + \
            self._fmt + StdoutFormatter.RST
        return logging.Formatter(fmt).format(record)


class Logger:
    """Logging class for SmartFlow software modules. Outputs messages
    to stdout, log file and also to MongoDB.

    Usage:
        logger = Logger.get('part_database')
        logger.info('info message')
    """
    _already_configured = []

    @classmethod
    def get(cls, name: str, mongoAddr='localhost') -> logging.Logger:
        """Returns a logger instance configured for SmartFlow.

        Args:
            name (str): software module name (e.g. 'part_database')

        Returns:
            logging.Logger: logger object. See
                https://docs.python.org/3/library/logging.html#logger-objects
        """
        logger = logging.getLogger(name)
        if name in cls._already_configured:
            return logger

        logger.setLevel(logging.DEBUG)

        cls._setup_stdout_logging(name)
        cls._setup_file_logging(name)
        cls._setup_mongo_logging(name, mongoAddr)

        cls._already_configured.append(name)
        return logger

    @staticmethod
    def _setup_stdout_logging(name):
        logger = logging.getLogger(name)

        handler = logging.StreamHandler(sys.stdout)
        formatter = StdoutFormatter(
            '[%(asctime)s] [%(filename)s:%(lineno)d] ' +
            '%(levelname)s %(message)s'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    @staticmethod
    def _setup_file_logging(name):
        logger = logging.getLogger(name)

        DEFAULT_PATH = os.path.join(os.getcwd(), 'logs')
        FILE_PATH = os.environ.get('LOGS_DIR', DEFAULT_PATH)
        os.makedirs(FILE_PATH, exist_ok=True)

        filename = os.path.join(FILE_PATH, f'{name}.log')

        handler = TimedRotatingFileHandler(
            filename,
            when='d',       # create a log file for every day
            backupCount=30  # keep logs for 30 days
        )

        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s %(filename)s:%(lineno)d] ' +
            '%(levelname)s %(message)s'
        )

        handler.setFormatter(formatter)

        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)

    @staticmethod
    def _setup_mongo_logging(name, addr):
        logger = logging.getLogger(name)
        logger.debug('connecting to MongoDB for logging')

        MONGO_URL = env.db("MONGO_URL", default=f"mongo://{addr}:27017")


        handler_params = {
            'level': logging.INFO,
            'host': MONGO_URL["HOST"],
            'port': MONGO_URL["PORT"],
            'username': MONGO_URL.get("USER"),
            'password': MONGO_URL.get("PASSWORD"),
            'database_name': MONGO_URL.get("NAME", "smartplay"),
            'authentication_db': MONGO_URL.get("NAME", "admin"),
            'fail_silently': True,      # do not throw exceptions if fails
            'formatter': MongoFormatter(),
            'connectTimeoutMS': 2000,           # how long to wait before error
            'serverSelectionTimeoutMS': 2000    # idem
        }

        try:
            handler = MongoHandler(**handler_params)
            handler.connection.list_database_names()
        except Exception as e:
            logger.error('failed to connect to MongoDB')
            logger.debug(e)
            params = ['host', 'port', 'database_name', 'username', 'password']
            vals = []
            for param in params:
                vals.append(f'{param}={handler_params[param]}')
            msg = 'MongoDB params: ' + ', '.join(vals)
            logger.debug(msg)
            return

        logger.info('connected to MongoDB')
        logger.addHandler(handler)
