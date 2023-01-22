import logging
import sys
from logging import Logger, Formatter, StreamHandler, FileHandler


class LoggerSetup:
    """
    Attributes:
        logger              (Logger)                : 需要设置的日志器
        save_log            (bool)                  : 是否保存日志

        formatter           (Formatter)             : 绑定的格式器
        stream_handler      (StreamHandler)         : 绑定的流式处理器
        file_handler        (FileHandler | None)    : 绑定的文件处理器
    """

    def __init__(self, logger: Logger,
                 fmt: str = "%(asctime)s|%(levelname)s|%(message)s",
                 datefmt: str = "%Y-%m-%d %H:%M:%S",
                 stream_level: int = logging.DEBUG,
                 file_level: int = logging.INFO):
        """
        根据传入的参数配置日志器
        并可以控制日志器运行与否

        Args:
            logger          (Logger)            : 需要设置的日志器
            fmt             (str)               : 日志输出信息格式
            datefmt         (str)               : 日志输出日期格式
        """

        self.logger: Logger = logger
        self.logger.setLevel(logging.DEBUG)
        self.save_log: bool = False

        self.formatter: Formatter = Formatter(fmt=fmt, datefmt=datefmt)

        self.stream_handler: StreamHandler = StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(self.formatter)
        self.stream_handler.setLevel(stream_level)
        self.logger.addHandler(self.stream_handler)

        self.file_handler: FileHandler = FileHandler(f"./bilianalyzer.log", mode='a', encoding="utf-8")
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(file_level)
        self.logger.addHandler(self.file_handler)
