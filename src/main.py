import asyncio
import logging
import os
import threading
import time

import bilibili_api.comment
from bilibili_api.comment import ResourceType

from analyzer import Analyzer
from constants import *
from database import DatabaseLoader, DatabaseDumper
from downloader import Downloader, PreProcessor
from progress import Progress


class DownloadThread(threading.Thread):
    def __init__(self, downloader: Downloader):
        threading.Thread.__init__(self)
        self.downloader = downloader

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.download())

    async def download(self):
        await self.downloader.download_pages()


class LogThread(threading.Thread):
    def __init__(self, progress: Progress, logger: logging.Logger, interval: float = 1.0, timeout: int = 10):
        threading.Thread.__init__(self)
        self.progress = progress
        self.interval = interval
        self.timeout = timeout
        self.logger = logger

    def run(self):
        timeout = self.timeout
        start_time = int(time.time())
        self.logger.info(f"{self.progress.name} {START_INFO_MSG}")
        while not self.progress.counter.have_finished:
            if self.progress.counter.have_started:
                self.logger.debug(f"{self.progress.name} {self.progress.counter.percentage}%")

            # 启动日志线程 但若处理未开始 则在超时后引发异常
            else:
                timeout -= 1
                if timeout < 0:
                    self.logger.error(TIMEOUT_ERROR_MSG)
                    raise TimeoutError

            time.sleep(self.interval)

        end_time = int(time.time())
        time_cost = end_time - start_time
        self.logger.info(f"{self.progress.name} {FINISH_INFO_MSG} {TIME_COST_MSG}: {time_cost}{TIME_COST_UNIT}")


if __name__ == "__main__":
    def main(oid: str, **kwargs):
        if kwargs["video"]:
            oid: int = bilibili_api.bvid2aid(oid)
            otype: ResourceType = ResourceType.VIDEO
        elif kwargs["dynamic"]:
            oid: int = int(oid)
            otype: ResourceType = ResourceType.DYNAMIC
        else:
            raise ValueError
        os.makedirs(kwargs["storage"], exist_ok=True)

        # 配置logger
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(fmt="%(asctime)s|%(levelname)s|%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler = logging.FileHandler(f"{kwargs['storage']}\\{oid}.log", mode='w', encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        # 输出 运行开始信息
        start_time = int(time.time())
        logger.info(f"{MAIN_NAME} {START_INFO_MSG} OID:{oid} Type:{otype.name.lower()}")

        if kwargs["all"]:
            download(oid, otype, kwargs["storage"], logger)
            preprocess(oid, kwargs["storage"], logger)
            analyze(oid, kwargs["storage"], logger)

        elif kwargs["download"]:
            download(oid, otype, kwargs["storage"], logger)

        elif kwargs["preprocess"]:
            preprocess(oid, kwargs["storage"], logger)

        elif kwargs["analyze"]:
            analyze(oid, kwargs["storage"], logger)

        # 输出 运行信息
        end_time = int(time.time())
        time_cost = end_time - start_time
        logger.info(f"{MAIN_NAME} {FINISH_INFO_MSG} {TIME_COST_MSG}: {time_cost}{TIME_COST_UNIT}")


    def download(oid: int, otype: ResourceType, path: str, logger: logging.Logger):
        downloader = Downloader(oid, otype, 0.4)
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")

        # 从网络API下载评论
        download_thread = DownloadThread(downloader)
        log_thread = LogThread(downloader, logger)
        log_thread.start()
        download_thread.start()
        download_thread.join()
        log_thread.join()

        # 存储 下载结果
        log_thread = LogThread(db_dumper, logger)
        log_thread.start()
        db_dumper.dump("Pages", downloader.pages)
        log_thread.join()


    def preprocess(oid, path, logger: logging.Logger):
        preprocessor = PreProcessor()
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")
        db_loader = DatabaseLoader(f"{path}\\{oid}.db")

        # 读取 下载结果
        log_thread = LogThread(db_loader, logger)
        log_thread.start()
        pages = db_loader.load("Pages")
        log_thread.join()

        # 处理 下载结果
        log_thread = LogThread(preprocessor, logger)
        log_thread.start()
        comments, users = preprocessor.pages_to_data(pages)
        log_thread.join()

        # 存储 处理结果
        log_thread = LogThread(db_dumper, logger)
        log_thread.start()
        db_dumper.dump("Comments", comments)
        log_thread.join()
        log_thread = LogThread(db_dumper, logger)
        log_thread.start()
        db_dumper.dump("Users", users)
        log_thread.join()


    def analyze(oid, path, logger: logging.Logger):
        analyzer = Analyzer()
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")
        db_loader = DatabaseLoader(f"{path}\\{oid}.db")

        # 读取 处理结果
        log_thread = LogThread(db_loader, logger)
        log_thread.start()
        comments = db_loader.load("Comments")
        log_thread.join()

        log_thread = LogThread(db_loader, logger)
        log_thread.start()
        users = db_loader.load("Users")
        log_thread.join()

        # 分析 处理结果
        log_thread = LogThread(analyzer, logger)
        analyzer.set_data(comments, users)
        log_thread.start()
        analyses = analyzer.analyze(Fields.ALL)
        log_thread.join()

        # 存储 分析结果
        log_thread = LogThread(db_dumper, logger)
        log_thread.start()
        db_dumper.dump("Analyses", analyses)
        log_thread.join()

    def args_space2dict(namespace):
        return {
            "id": namespace.id,

            "download": namespace.download,
            "preprocess": namespace.preprocess,
            "analyze": namespace.analyze,
            "all": namespace.all,

            "dynamic": namespace.dynamic,
            "video": namespace.video,

            "storage": namespace.storage,
            "quiet": namespace.quiet
        }
    import argparse

    argparser = argparse.ArgumentParser()
    operations = argparser.add_mutually_exclusive_group(required=False)
    resources = argparser.add_mutually_exclusive_group(required=False)
    argparser.add_argument("id", type=str,
                           help=ID_HELP)

    # 操作
    operations.add_argument("-d", "--download", action="store_true",
                            help=ACTION_HELP["download"])
    operations.add_argument("-p", "--preprocess", action="store_true",
                            help=ACTION_HELP["preprocess"])
    operations.add_argument("-a", "--analyze", action="store_true",
                            help=ACTION_HELP["analyze"])
    operations.add_argument("-A", "--all", action="store_true",
                            help=ACTION_HELP["all"])

    resources.add_argument("-D", "--dynamic", action="store_true",
                           help=OTYPE_HELP["dynamic"])
    resources.add_argument("-V", "--video", action="store_true",
                           help=OTYPE_HELP["video"])

    argparser.add_argument("-s", "--storage", type=str, default=".\\storage",
                           help=OPT_HELP["sort"])
    argparser.add_argument("-q", "--quiet", action="store_true",
                           help=OPT_HELP["quiet"])

    args = args_space2dict(argparser.parse_args())
    main(args["id"], **args)
