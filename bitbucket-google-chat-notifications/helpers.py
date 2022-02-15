import logging


def config_logger(level: int = logging.WARNING) -> None:
    _format = "[%(asctime)s] %(levelname)s %(module)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(_format, datefmt=date_format)

    logger = logging.getLogger("bbgc")
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
