import logging, inspect

def get_logger(str_level='info', name=__name__):
    level = getattr(logging, str_level.upper())
    # Create a custom logger
    logger = logging.getLogger(name)
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

    def log(level: str, *args, sep=None) -> None:
        caller_name = inspect.stack()[1].function
        log_func = getattr(logger, level)
        if not sep:
            sep = ' - ' if len(args) == 1 else '\n  '
        log_str = f"{caller_name}" + f"{sep}%s"* len(args)
        log_func(log_str, *args)

    return logger, log

