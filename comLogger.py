import logging



logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('logs/flask.log', encoding='utf-8') # creates handler for the log file
logger.addHandler(handler)


def __init__() -> None:
    
    pass


def get_logger():
    return logger
