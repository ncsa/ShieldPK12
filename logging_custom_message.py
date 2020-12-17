import logging
from time import gmtime

# Let's log
logging.Formatter.converter = gmtime
json_formatter = "{'timestamp':'%(asctime)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=json_formatter, level=logging.INFO)


def logging_custom_message(message):
    logging.info(message)
    return None
