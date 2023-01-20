import json
import logging
import os
import sys
import threading
import time
from collections import OrderedDict
from typing import Callable, Literal

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QTableWidgetItem
from bilibili_api import Credential, ResponseCodeException
from bilibili_api.comment import CommentResourceType

from analyze import UserAnalyzer
from config import Configer, Config
from convert import convert_video_id
from download import CommentDownloader
from exceptions import CheckingException
from log import LoggerSetup
from signals import ui_signals
from ui.ui_about import Ui_AboutWiindow
from ui.ui_config import Ui_ConfigWindow
from ui.ui_main import Ui_MainWindow
from ui.ui_tutorial import Ui_TutorialWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.configer = Configer()
        self.logger = logging.getLogger("main")
        self.logger_setup = LoggerSetup(self.logger,
                                        self.configer.config.log_path)
        self.logger_setup.set_file_log(self.configer.config.save_log)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind()
        self.sub_windows = {
            "config": None,
            "about": None,
            "tutorial": None
        }
        self.analyze_result: OrderedDict | None = None
        self.cmtfile_path: str = ""

    def bind(self):
        # 转换页
        self.ui.convertButton.clicked.connect(self.handle_convert)
        self.ui.copyButton.clicked.connect(self.handle_copy)

        # 下载页
        self.ui.downloadButton.clicked.connect(self.handle_download)
        self.ui.analyzeCmtfileButton.clicked.connect(self.select_cmtfile_path)

        # 分析页
        self.ui.analyzeRunButton.clicked.connect(self.handle_analyze)
        self.ui.analyzeExportButton.clicked.connect(self.export_analyze_result)

        # 菜单栏
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionConfig.triggered.connect(self.start_window("config"))
        self.ui.actionAbout.triggered.connect(self.start_window("about"))
        self.ui.actionTutorial.triggered.connect(self.start_window("tutorial"))

        # 自定义信号
        ui_signals.updateDownloadProgress.connect(self.update_download_progress)
        ui_signals.updateAnalyzeProgress.connect(self.update_analyze_progress)
        ui_signals.callErrorBox.connect(self.call_error_box)
        ui_signals.showAnalyzeResult.connect(self.show_analyze_result)

    def handle_convert(self):
        sid = self.ui.convertInput.text()

        try:
            res = convert_video_id(sid)
            self.ui.convertOutput.setReadOnly(False)
            self.ui.convertOutput.setText(res)
            self.ui.convertOutput.setReadOnly(True)

        except (ValueError, TypeError) as error:
            call_msg_box(self, str(error))

    def handle_copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.convertOutput.text())
        call_msg_box(self, "复制成功", "information")

    def handle_download(self):
        def get_info_ui():
            oid = self.ui.idEntry.text()
            otype = {
                "视频": CommentResourceType.VIDEO,
                "动态": CommentResourceType.DYNAMIC,
                "画册": CommentResourceType.DYNAMIC_DRAW
            }[self.ui.typeBox.currentText()]
            start = self.ui.startBox.value()
            end = self.ui.endBox.value()
            step = self.ui.stepBox.value()
            indexes = range(start, end, step)

            return {
                "oid": oid,
                "otype": otype,
                "indexes": indexes
            }

        def download():
            try:
                start_time = int(time.time())
                downloader.download()
                end_time = int(time.time())
                self.logger.info(f"下载完毕 用时{end_time - start_time}秒")
                serializable_comments = downloader.serializable_comments(key="rpid")

                current_download_path = f"{self.configer.config.download_path}/{info['oid']}"
                current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                os.makedirs(current_download_path, exist_ok=True)
                with open(f"{current_download_path}/comments_{current_time}.json".replace("\\", "/"), "w",
                          encoding="utf-8") as f:
                    json.dump(serializable_comments, f, indent=4, ensure_ascii=False)
                cmtfile_path = f"{current_download_path}/comments_{current_time}.json".replace("\\", "/")
                self.cmtfile_path = cmtfile_path
                self.logger.info(f"保存完毕 保存位置:{self.cmtfile_path}")
                self.show_cmtfile_path()

            except (ResponseCodeException, CheckingException) as download_error:
                self.logger.warning(f"下载失败 失败原因:\n"
                                    f"{str(download_error)}")
                ui_signals.callErrorBox.emit(download_error)

            finally:
                self.ui.downloadButton.setEnabled(True)

        info = get_info_ui()
        credential = self.configer.credential
        downloader = CommentDownloader(**info, credential=credential,
                                       progress_signal=ui_signals.updateDownloadProgress)

        self.logger.info(f"开始下载 下载参数:\n"
                         f"资源ID:{info['oid']}\n"
                         f"资源类型:{info['otype'].name}\n"
                         f"索引范围:{info['indexes']}")

        # TODO: 优化检查结构
        # 检查下载准备是否完成
        try:
            self.logger.debug(f"当前设置:\n"
                              f"{str(self.configer)}")
            downloader.check_arguments()
            self.configer.check_download_path()
            thread = threading.Thread(target=download)
            thread.start()

        except (ValueError, FileNotFoundError) as error:
            call_msg_box(self, str(error))
            self.logger.warning(str(error))

        else:
            self.ui.downloadButton.setEnabled(False)
            self.ui.downloadProgress.setMaximum(downloader.maximum_progress)
            self.ui.downloadProgress.setVisible(True)

    def handle_analyze(self):
        # TODO: 优化加载顺序
        # TODO: 增加导入本地评论功能
        # TODO: 增加日志输出
        # TODO: 添加分析计时功能

        def analyze():
            # TODO: 自适应结果列宽度
            # TODO: 修复评论者关注功能
            # TODO: 可调前N项
            analyze_mode = {
                "评论者粉丝牌": "FanMedal",
                "评论者关注": "Followings"
            }[self.ui.analyzeModeBox.currentText()]

            result: OrderedDict = analyzer.get_top_result(analyzer.analyze(analyze_mode), 500)
            ui_signals.showAnalyzeResult.emit(result)
            self.logger.info("分析完成")
            self.analyze_result = result

        if self.ui.analyzeCmtfileInput.text() != "":
            self.cmtfile_path = self.ui.analyzeCmtfileInput.text()

        self.logger.info(f"读取评论:\n"
                         f"评论文件路径:\n"
                         f"{self.cmtfile_path}")
        if not os.path.exists(self.cmtfile_path):
            call_msg_box(self, str("请先指定有效的评论文件"))

        analyzer = UserAnalyzer(credential=self.configer.credential,
                                progress_signal=ui_signals.updateAnalyzeProgress)
        analyzer.import_from_comments(self.cmtfile_path)
        self.logger.info("读取完成开始分析")
        self.ui.analyzeProgress.setMaximum(analyzer.maximum_progress)
        thread = threading.Thread(target=analyze)
        thread.start()

    def show_analyze_result(self, result: OrderedDict):
        self.ui.analyzeTable.setRowCount(len(result))
        self.ui.analyzeTable.setColumnCount(2)
        self.ui.analyzeTable.setHorizontalHeaderLabels(["粉丝牌/关注", "出现次数"])
        self.ui.analyzeTable.setColumnWidth(0, 10)
        self.ui.analyzeTable.setColumnWidth(1, 10)

        for index, (name, count) in enumerate(result.items()):
            self.ui.analyzeTable.setItem(index, 0, QTableWidgetItem(str(name)))
            self.ui.analyzeTable.setItem(index, 1, QTableWidgetItem(str(count)))
        self.ui.analyzeTable.show()

    def export_analyze_result(self):
        if self.analyze_result is None:
            call_msg_box(self, "请先分析才能进行导出")
            return
        self.logger.info("开始保存分析结果")
        filepath, filetype = QFileDialog.getSaveFileName(self, filter="json文件 (*.json)")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.analyze_result, f, indent=4, ensure_ascii=False)
        self.logger.info(f"保存完毕 保存位置: {filepath}")

    def show_cmtfile_path(self):
        self.ui.analyzeCmtfileInput.setText(self.cmtfile_path)

    def select_cmtfile_path(self):
        filepath, filetype = QFileDialog.getOpenFileName(self)
        if os.path.exists(filepath):
            self.cmtfile_path = filepath
        self.show_cmtfile_path()

    def update_download_progress(self, value: int):
        self.ui.downloadProgress.setValue(value)

    def update_analyze_progress(self, value: int):
        self.ui.analyzeProgress.setValue(value)

    def call_error_box(self, error: Exception):
        call_msg_box(self, str(error))

    def start_window(self,
                     window_name: Literal["config", "about", "tutorial"]) \
            -> Callable[[None], None]:
        def start_wrapper():
            if self.sub_windows[window_name] is None:
                self.sub_windows[window_name] = sub_window
            self.sub_windows[window_name].show()

        def coming_soon_wrapper():
            call_msg_box(self, "即将到来", level="information")

        if window_name == "config":
            sub_window = ConfigWindow(self)
            return start_wrapper
        elif window_name == "about":
            sub_window = AboutWindow(self)
            return start_wrapper
        elif window_name == "tutorial":
            sub_window = TutorialWindow(self)
            return start_wrapper
        else:
            return coming_soon_wrapper


class ConfigWindow(QWidget):
    def __init__(self, main_window: MainWindow):
        super(ConfigWindow, self).__init__()
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.configer = self.main_window.configer
        self.bind()
        self.show_config()
        self.show_credential()

    def bind(self):
        self.ui.confirmButton.accepted.connect(self.confirm_accepted)
        self.ui.confirmButton.rejected.connect(self.confirm_rejected)
        self.ui.scanButton.clicked.connect(self.scan_credential)
        self.ui.importButton.clicked.connect(self.import_credential)
        self.ui.exportButton.clicked.connect(self.export_credential)
        self.ui.downloadTool.clicked.connect(self.select_download_path)
        self.ui.logpathTool.clicked.connect(self.select_log_path)

    def show_config(self):
        # 在UI上显示设置
        self.ui.downloadEntry.setText(self.configer.config.download_path)
        self.ui.logCheckBox.setChecked(self.configer.config.save_log)
        self.ui.logpathEntry.setText(self.configer.config.log_path)
        self.ui.logpathEntry.setEnabled(self.ui.logCheckBox.isChecked())

    def show_credential(self):
        # 在UI上显示凭证
        credential = self.configer.credential
        if credential.sessdata is not None:
            self.ui.sessdataEntry.setText(credential.sessdata)
        if credential.bili_jct is not None:
            self.ui.bilijctEntry.setText(credential.bili_jct)
        if credential.buvid3 is not None:
            self.ui.buvid3Entry.setText(credential.buvid3)

    def read_config(self):
        # 从UI上读取设置
        self.configer.config = Config(
            download_path=self.ui.downloadEntry.text(),
            save_log=self.ui.logCheckBox.isChecked(),
            log_path=self.ui.logpathEntry.text()
        )

    def read_credential(self):
        # 从UI上读取凭证
        self.configer.credential = Credential(
            sessdata=self.ui.sessdataEntry.text() if self.ui.sessdataEntry.text() != "" else None,
            bili_jct=self.ui.bilijctEntry.text() if self.ui.bilijctEntry.text() != "" else None,
            buvid3=self.ui.buvid3Entry.text() if self.ui.buvid3Entry.text() != "" else None
        )

    def confirm_accepted(self):
        self.read_config()
        self.read_credential()
        self.main_window.logger.debug(f"当前设置:\n"
                                      f"{str(self.configer)}")
        try:
            self.configer.check_log_path()
        except FileNotFoundError as error:
            call_msg_box(self, str(error))
            return

        self.configer.dump_to_file()

        self.close()

    def confirm_rejected(self):
        self.close()

    def scan_credential(self):
        self.configer.scan_credential()

        credential = self.configer.credential
        if credential.sessdata is not None:
            self.ui.sessdataEntry.setText(credential.sessdata)
        if credential.bili_jct is not None:
            self.ui.bilijctEntry.setText(credential.bili_jct)
        if credential.buvid3 is not None:
            self.ui.buvid3Entry.setText(credential.buvid3)

    def import_credential(self):
        try:
            filepath, filetype = QFileDialog.getOpenFileName(self)
            if os.path.exists(filepath):
                self.configer.import_credential(filepath)
            elif filepath == "":
                pass
        except FileNotFoundError:
            call_msg_box(self, "文件不存在")
        except (TypeError | ValueError):
            call_msg_box(self, "文件格式错误")
        self.show_credential()

    def export_credential(self):
        filepath, filetype = QFileDialog.getSaveFileName(self)
        self.read_credential()
        if filepath == "":
            pass
        else:
            self.configer.export_credential(filepath)

    def select_download_path(self):
        filepath = QFileDialog.getExistingDirectory(self)
        if filepath != "":
            self.configer.config.download_path = filepath
        self.show_config()

    def select_log_path(self):
        filepath = QFileDialog.getExistingDirectory(self)
        if filepath != "":
            self.configer.config.log_path = filepath
        self.show_config()


class AboutWindow(QWidget):
    def __init__(self, main_window: MainWindow):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutWiindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.bind()
        self.load_content("./docs/about.html")

    def bind(self):
        pass

    def load_content(self, content_path: str):
        if os.path.exists(content_path):
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.ui.textBrowser.setText(content)
        else:
            self.ui.textBrowser.setText("Coming Soon")


class TutorialWindow(QWidget):
    def __init__(self, main_window: MainWindow):
        super(TutorialWindow, self).__init__()
        self.ui = Ui_TutorialWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.bind()
        self.load_content("./docs/tutorial.html")

    def bind(self):
        pass

    def load_content(self, content_path: str):
        if os.path.exists(content_path):
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.ui.textBrowser.setText(content)
        else:
            self.ui.textBrowser.setText("Coming Soon")


def call_msg_box(parent: QWidget, content: str,
                 level: Literal["information", "warning"] = "warning"):
    if level == "information":
        QMessageBox.information(parent, "提示", content, QMessageBox.Yes)
    elif level == "warning":
        QMessageBox.warning(parent, "警告", content, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
