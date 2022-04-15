import logging

def get_logger(str_level='info'):
    level = getattr(logging, str_level.upper())
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('md2anki.log', 'w')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(levelname)s:%(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger
