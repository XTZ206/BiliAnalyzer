import logging
import sys
from logging import Logger, Formatter, StreamHandler, FileHandler
import os
from os import PathLike


class LoggerSetup:
    """
    Attributes:
        logger              (Logger)                : 需要设置的日志器
        log_path            (PathLike[str])         : 日志保存的路径
        save_log            (bool)                  : 是否保存日志

        formatter           (Formatter)             : 绑定的格式器
        stream_handler      (StreamHandler)         : 绑定的流式处理器
        file_handler        (FileHandler | None)    : 绑定的文件处理器
    """

    def __init__(self, logger: Logger,
                 log_path: PathLike[str] | None = None,
                 fmt: str = "%(asctime)s|%(levelname)s|%(message)s",
                 datefmt: str = "%Y-%m-%d %H:%M:%S",
                 stream_level=logging.DEBUG):
        """
        根据传入的参数配置日志器
        并可以控制日志器运行与否

        Args:
            logger          (Logger)            : 需要设置的日志器
            log_path        (PathLike[str])     : 日志保存的路径
            fmt             (str)               : 日志输出信息格式
            datefmt         (str)               : 日志输出日期格式
        """

        self.logger: Logger = logger
        self.logger.setLevel(logging.DEBUG)
        self.log_path: PathLike[str] = log_path
        self.save_log: bool = False

        self.formatter: Formatter = Formatter(fmt=fmt, datefmt=datefmt)
        self.stream_handler: StreamHandler = StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(self.formatter)
        self.stream_handler.setLevel(stream_level)
        self.logger.addHandler(self.stream_handler)
        self.file_handler: FileHandler | None = None

    def set_file_log(self, save_log: bool,
                     log_path: PathLike[str] | None = None,
                     file_level=logging.INFO):
        """
        打开或关闭文件日志 或是设置文件日志的日志等级和保存路径
        Args:
            save_log        (bool)                  : 是否开启文件日志
            log_path        (PathLike[str]|None)    : 文件日志的保存路径 None则表示不改变. Defaults to None.
            file_level      (int)                   : 文件日志的日志等级
        """

        if save_log is True:

            # Case: 打开文件日志(使用默认文件路径) ON/OFF -> ON
            if log_path is None and os.path.exists(self.log_path):
                self.save_log = save_log
                self._bind_file_handler()
                self.file_handler.setLevel(file_level)
            # Case: 打开文件日志(使用新文件路径) OLD/OFF -> NEW
            elif log_path is not None and os.path.exists(log_path):
                self.log_path = log_path
                self.save_log = save_log
                self._remove_file_handler()
                self._bind_file_handler()
                self.file_handler.setLevel(file_level)

        elif self.save_log is True:
            # Case: 关闭文件日志 ON -> OFF
            self.logger.removeHandler(self.file_handler)
            self.save_log = save_log
            self.log_path = self.log_path if log_path is None else log_path

    def _bind_file_handler(self):
        """
        绑定文件处理器 防止重复
        """
        if self.file_handler is None:
            self.file_handler = FileHandler(f"{self.log_path}/bilianalyzer.log",
                                            mode='a', encoding="utf-8")
            self.file_handler.setFormatter(self.formatter)

        if self.file_handler not in self.logger.handlers:
            self.logger.addHandler(self.file_handler)

    def _remove_file_handler(self):
        """
        去除文件处理器
        """
        if self.file_handler is not None:
            self.logger.removeHandler(self.file_handler)
            self.file_handler = None
