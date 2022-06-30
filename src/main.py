import asyncio
import threading
import time
from typing import Optional

import bilibili_api.comment

from analyzer import Analyzer, Fields
from database import DatabaseLoader, DatabaseDumper
from downloader import Downloader, Processor
from progress import Progress, Logger


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


class ProgressThread(threading.Thread):
    def __init__(self, progress: Progress, logger: Optional[Logger] = None, interval: float = 0.5):
        threading.Thread.__init__(self)
        self.progress = progress
        self.progress_counter = progress.progress_counter
        self.interval = interval
        self.logger = logger

    def run(self):
        progress_counter = self.progress_counter
        while not progress_counter.have_finished:
            if progress_counter.have_started:
                print(f"\r{time.strftime('%H:%M:%S', time.localtime())} {progress_counter.progress_str}", end="")
            time.sleep(self.interval)
        log = f"{time.strftime('%H:%M:%S', time.localtime())} {progress_counter.progress_str}"
        print('\r' + log)
        if self.logger is not None:
            self.logger.add_to_log(log)


if __name__ == "__main__":
    def main(bvid, args):
        oid = bilibili_api.bvid2aid(bvid)

        logger = Logger(f"storage\\{oid}.log")

        # 输出 运行开始信息
        start_time = time.localtime()
        log = f"{time.strftime('%H:%M:%S', start_time)} Started OID:{oid} BVID: {bvid}"
        print(log)
        logger.add_to_log(log)

        if args.all:
            download(oid, args.storage, logger)
            process(oid, args.storage, logger)
            analyze(oid, args.storage, logger)

        elif args.download:
            download(oid, args.storage, logger)

        elif args.process:
            process(oid, args.storage, logger)
        elif args.analyze:
            analyze(oid, args.storage, logger)

        # 输出 运行信息
        end_time = time.localtime()
        used_time = int(time.mktime(end_time) - time.mktime(start_time))
        log = f"{time.strftime('%H:%M:%S', end_time)} Finished"
        print(log)
        logger.add_to_log(log)
        log = f"{time.strftime('%H:%M:%S', end_time)} Used time: {used_time} seconds"
        print(log)
        logger.add_to_log(log)
        logger.save_log()


    def download(oid, path, logger=None):
        downloader = Downloader(oid, bilibili_api.comment.ResourceType.VIDEO, 0.4)
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")

        # 从网络API下载评论
        download_thread = DownloadThread(downloader)
        progress_thread = ProgressThread(downloader, logger)
        progress_thread.start()
        download_thread.start()
        download_thread.join()
        progress_thread.join()

        # 存储 下载结果
        progress_thread = ProgressThread(db_dumper, logger)
        progress_thread.start()
        db_dumper.dump("Pages", downloader.pages)
        progress_thread.join()


    def process(oid, path, logger=None):
        processor = Processor()
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")
        db_loader = DatabaseLoader(f"{path}\\{oid}.db")

        # 读取 下载结果
        progress_thread = ProgressThread(db_loader, logger)
        progress_thread.start()
        pages = db_loader.load("Pages")
        progress_thread.join()

        # 处理 下载结果
        progress_thread = ProgressThread(processor, logger)
        progress_thread.start()
        comments, users = processor.pages_to_data(pages)
        progress_thread.join()

        # 存储 处理结果
        progress_thread = ProgressThread(db_dumper, logger)
        progress_thread.start()
        db_dumper.dump("Comments", comments)
        progress_thread.join()
        progress_thread = ProgressThread(db_dumper, logger)
        progress_thread.start()
        db_dumper.dump("Users", users)
        progress_thread.join()


    def analyze(oid, path, logger=None):
        analyzer = Analyzer()
        db_dumper = DatabaseDumper(f"{path}\\{oid}.db")
        db_loader = DatabaseLoader(f"{path}\\{oid}.db")

        # 读取 处理结果
        progress_thread = ProgressThread(db_loader, logger)
        progress_thread.start()
        comments = db_loader.load("Comments")
        progress_thread.join()

        progress_thread = ProgressThread(db_loader, logger)
        progress_thread.start()
        users = db_loader.load("Users")
        progress_thread.join()

        # 分析 处理结果
        progress_thread = ProgressThread(analyzer, logger)
        analyzer.set_data(comments, users)
        progress_thread.start()
        analyses = analyzer.analyze(Fields.ALL)
        progress_thread.join()

        # 存储 分析结果
        progress_thread = ProgressThread(db_dumper, logger)
        progress_thread.start()
        db_dumper.dump("Analyses", analyses)
        progress_thread.join()


    import argparse

    argparser = argparse.ArgumentParser()
    actions = argparser.add_mutually_exclusive_group()
    argparser.add_argument("bvid", type=str,
                           help="the bvid of video you want to analyze")
    actions.add_argument("-d", "--download", action="store_true",
                         help="just download the comments")
    actions.add_argument("-p", "--process", action="store_true",
                         help="just process the comments")
    actions.add_argument("-a", "--analyze", action="store_true",
                         help="just analyze the comments")
    actions.add_argument("-A", "--all", action="store_true", default=True,
                         help="download, process and analyze the comments")
    argparser.add_argument("-s", "--storage", type=str, default=".\\storage",
                           help="where you want to store the results")
    argparser.add_argument("-q", "--quiet", action="store_true",
                           help="stop printing log on the screen")

    args = argparser.parse_args()
    main(args.bvid, args)