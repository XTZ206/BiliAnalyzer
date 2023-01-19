import logging
from os import PathLike


def setup_logger(logger: logging.Logger, log_path: PathLike[str], save_log: bool):
    # TODO: 补充注释
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s|%(levelname)s|%(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if save_log:
        file_handler = logging.FileHandler(f"{log_path}/BiliAnalyzer.log", mode='a', encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
