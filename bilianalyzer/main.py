import logging
import os
import sys
import threading
import time
from collections import OrderedDict
from typing import Callable, Literal

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QTableWidgetItem, \
    QProgressBar, QHeaderView, QLineEdit
from bilibili_api import Credential
from bilibili_api.comment import CommentResourceType
from bilibili_api.user import User

from bilianalyzer.config import Configer, Config
from bilianalyzer.convert import convert_video_id, convert_comments_to_uids
from bilianalyzer.download import CommentDownloader, UserDownloader
from bilianalyzer.exceptions import FileNotSelectedException, AnalyzerException, FileFormatException
from bilianalyzer.log import LoggerSetup
from bilianalyzer.pipes import CmtFilePipe, UidFilePipe, UsrFilePipe, ResFilePipe, SwdFilePipe
from bilianalyzer.signals import ui_signals
from bilianalyzer.statistics import StatisticsMode, UsersStatistician, CommentsStatistician
from bilianalyzer.ui.ui_about import Ui_AboutWindow
from bilianalyzer.ui.ui_config import Ui_ConfigWindow
from bilianalyzer.ui.ui_main import Ui_MainWindow
from bilianalyzer.ui.ui_tutorial import Ui_TutorialWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.configer = Configer()
        self.logger = logging.getLogger("main")
        self.logger_setup = LoggerSetup(self.logger)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind()
        self.sub_windows = {
            "config": None,
            "about": None,
            "tutorial": None
        }

        self.analyze_in_path: str = ""
        self.analyze_out_path: str = ""
        self.statistics_in_path: str = ""
        self.statistics_result: OrderedDict | None = None

    def bind(self):
        # 转换页
        self.ui.convertRunButton.clicked.connect(self.handle_convert)
        self.ui.convertCopyButton.clicked.connect(self.handle_copy)

        # 下载页
        self.ui.downloadRunButton.clicked.connect(self.handle_download)

        # 分析页
        self.ui.analyzeCmtfileInput.textEdited.connect(self.read_file_path)
        self.ui.analyzeUsrfileInput.textEdited.connect(self.read_file_path)
        self.ui.analyzeCmtfileButton.clicked.connect(self.select_analyze_cmtfile)
        self.ui.analyzeUsrfileButton.clicked.connect(self.select_analyze_usrfile)
        self.ui.analyzeExportButton.clicked.connect(self.export_analyze_uidfile)
        self.ui.analyzeRunButton.clicked.connect(self.handle_analyze)

        # 统计页
        self.ui.statisticsFileInput.textEdited.connect(self.read_file_path)
        self.ui.statisticsFileButton.clicked.connect(self.select_statistics_srcfile)
        self.ui.statisticsRunButton.clicked.connect(self.handle_statistics)
        self.ui.statisticsExportButton.clicked.connect(self.export_statistics_resfile)
        self.ui.statisticsTypeBox.currentIndexChanged.connect(self.show_statistics_property)

        # 菜单栏
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionConfig.triggered.connect(self.start_window("config"))
        self.ui.actionAbout.triggered.connect(self.start_window("about"))
        self.ui.actionTutorial.triggered.connect(self.start_window("tutorial"))

        # 自定义信号
        ui_signals.updateProgressBar.connect(self.update_progress_bar)
        ui_signals.setProgressBar.connect(self.set_progress_bar)
        ui_signals.callErrorBox.connect(self.call_error_box)
        ui_signals.showStatisticsResult.connect(self.show_statistics_result)

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
        def get_args_ui():
            oid = self.ui.downloadOidInput.text()
            otype = {
                "视频": CommentResourceType.VIDEO,
                "动态": CommentResourceType.DYNAMIC,
                "画册": CommentResourceType.DYNAMIC_DRAW
            }[self.ui.downloadOtypeInput.currentText()]
            start = self.ui.downloadStartInput.value()
            end = self.ui.downloadEndInput.value()
            step = self.ui.downloadStepInput.value()
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
                if downloader.has_error_logs():
                    self.logger.warning(f"下载错误: \n"
                                        f"{downloader.get_error_logs_serialized()}")

                pipe.dump(downloader.get_storages(key="rpid"))
                self.logger.info(f"保存完毕 保存位置:{pipe.filepath}")

                # 自动将下载的评论文件传入分析模块
                self.analyze_in_path = pipe.filepath
                self.show_file_path()

            except AnalyzerException as download_error:
                self.logger.warning(f"下载失败: \n"
                                    f"{downloader.get_error_logs_serialized()}")
                ui_signals.callErrorBox.emit(download_error)

            finally:
                self.ui.downloadRunButton.setEnabled(True)

        try:
            # 获取参数并检查参数是否有效
            args = get_args_ui()
            if not args["oid"].isdigit():
                raise ValueError("资源ID必须为数字")
            if len(args["indexes"]) == 0:
                raise ValueError("索引范围不能为空")
            if not os.path.exists(self.configer.config.result_path):
                raise FileNotSelectedException("未指定下载路径")
            # 根据参数生成文件管道
            current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            download_out_dir = f"{self.configer.config.result_path}/{args['oid']}"
            download_out_path = f"{download_out_dir}/{current_time}.cmt".replace("\\", "/")
            os.makedirs(download_out_dir, exist_ok=True)
            pipe = CmtFilePipe(download_out_path, "w")
            # 生成下载器
            downloader = CommentDownloader(**args, credential=self.configer.credential,
                                           progress_signal=ui_signals.updateProgressBar)
            # 记录开始下载
            self.logger.info(f"开始下载 下载参数:\n"
                             f"资源ID:{args['oid']}\n"
                             f"资源类型:{args['otype'].name}\n"
                             f"索引范围:{args['indexes']}\n"
                             f"下载数量:{len(args['indexes'])}\n"
                             f"预计用时:{int(len(args['indexes']) * 1.1)}")

            # 在子线程进行下载
            thread = threading.Thread(target=download)
            thread.start()

        except (ValueError, AnalyzerException) as error:
            # 参数错误 提示并记入日志
            call_msg_box(self, str(error))
            self.logger.warning(str(error))

        else:
            # 参数有效 设置UI
            self.ui.downloadRunButton.setEnabled(False)
            self.ui.downloadProgress.setMaximum(downloader.maximum_progress)

    def handle_analyze(self):
        def analyze():
            try:
                start_time = int(time.time())
                downloader.download()
                end_time = int(time.time())
                self.logger.info(f"分析完毕 用时{end_time - start_time}秒")
                if downloader.has_error_logs():
                    self.logger.warning(f"下载错误: \n"
                                        f"{downloader.get_error_logs_serialized()}")

                pipe_out.dump(downloader.get_storages(key="uid"))
                self.logger.info(f"保存完毕 保存位置:{pipe_out.filepath}")
                self.statistics_in_path = self.analyze_out_path
                self.show_file_path()

            except AnalyzerException as analyze_error:
                self.logger.warning(f"分析失败: \n"
                                    f"{downloader.get_error_logs_serialized()}")
                ui_signals.callErrorBox.emit(analyze_error)
            finally:
                self.ui.analyzeRunButton.setEnabled(True)

        try:
            self.read_file_path()
            if self.analyze_in_path == "" or self.analyze_out_path == "":
                raise FileNotSelectedException("请选择输入和输出的文件路径")

            pipe_in = CmtFilePipe(self.analyze_in_path, "r")
            pipe_out = UsrFilePipe(self.analyze_out_path, "w")

            comments = pipe_in.load()
            uids = convert_comments_to_uids(comments)
            percentage = self.ui.analyzePercentageBox.value() / 100
            users = [User(uid) for uid in uids][::int(1 / percentage)] if percentage > 0 else []
            downloader = UserDownloader(users, credential=self.configer.credential,
                                        progress_signal=ui_signals.updateProgressBar)

            self.logger.info(f"开始分析 分析参数:\n"
                             f"处理数量:{len(uids)}\n"
                             f"筛选比例:{percentage}\n"
                             f"分析数量:{len(users)}\n"
                             f"预计用时:{int(len(users) * 1.1)}")

            thread = threading.Thread(target=analyze)
            thread.start()

        except AnalyzerException as error:
            call_msg_box(self, str(error))

        else:
            self.ui.analyzeProgress.setValue(0)
            self.ui.analyzeProgress.setMaximum(downloader.maximum_progress)
            self.ui.analyzeRunButton.setEnabled(False)

    def handle_statistics(self):
        # TODO: 可调tops值
        def get_args_ui():

            statistics_type = self.ui.statisticsTypeBox.currentText()
            statistics_property = self.ui.statisticsPropertyBox.currentText()
            statistics_show = {
                False: "标准模式",
                True: "昵称模式"
            }[self.ui.statisticsShowBox.isChecked()]
            statistics_mode = {
                "用户性别": StatisticsMode.SEX,
                "用户生日": StatisticsMode.BIRTHDAY,
                "用户学校": StatisticsMode.SCHOOL,
                "用户专业": StatisticsMode.PROFESSION,
                "用户UID位数": StatisticsMode.UID,
                "用户等级": StatisticsMode.LEVEL,
                "用户大会员": StatisticsMode.VIP,
                "用户标签": StatisticsMode.TAGS,
                "用户装扮": StatisticsMode.PENDANT,
                "用户名牌": StatisticsMode.NAMEPLATE,
                "用户关注": StatisticsMode.FOLLOWING,
                "用户粉丝牌": StatisticsMode.FAN_MEDALS,
                "评论内容": StatisticsMode.CONTENT,
                "评论表情(评论数)": StatisticsMode.EMOTES_UNREPEATABLE,
                "评论表情(个数)": StatisticsMode.EMOTES_REPEATABLE
            }[statistics_type + statistics_property]
            statistics_headers = {
                "用户性别": ["性别", "出现次数"],
                "用户生日": ["生日", "出现次数"],
                "用户学校": ["学校", "出现次数"],
                "用户专业": ["专业", "出现次数"],
                "用户UID位数": ["UID位数", "出现次数"],
                "用户等级": ["等级", "出现次数"],
                "用户大会员": ["大会员", "出现次数"],
                "用户标签": ["标签", "出现次数"],
                "用户装扮": ["装扮", "出现次数"],
                "用户名牌": ["名牌", "出现次数"],
                "用户关注": ["关注", "出现次数"],
                "用户粉丝牌": ["粉丝牌", "出现次数"],
                "评论内容": ["内容", "出现次数"],
                "评论表情(评论数)": ["表情", "出现次数"],
                "评论表情(个数)": ["表情", "出现次数"]
            }[statistics_type + statistics_property]

            return {
                "type": statistics_type,
                "property": statistics_property,
                "show": statistics_show,
                "mode": statistics_mode,
                "headers": statistics_headers
            }

        def statistics():
            try:
                start_time = int(time.time())
                if args["type"] == "用户":
                    statistics_result: OrderedDict = \
                        statistician.statistics(args["mode"], tops=100,
                                                output_name=(args["show"] == "昵称模式"))
                elif args["type"] == "评论":
                    statistics_result: OrderedDict = \
                        statistician.statistics(args["mode"], tops=100,
                                                stopwords=pipe_stop.load())
                else:
                    raise AnalyzerException(f"不存在的统计类型{args['type']}")

                ui_signals.showStatisticsResult.emit(statistics_result, args["headers"])
                end_time = int(time.time())
                self.logger.info(f"统计完成 用时{end_time - start_time}秒 共统计数据{len(statistician.data)}条")
                self.statistics_result = statistics_result
                if args["show"] == "标准模式":
                    ui_signals.updateProgressBar.emit(100, "统计")

            # TODO: 使用积累错误记录
            except AnalyzerException as statistics_error:
                if statistician.current_progress < 1:
                    error_location = "0"
                else:
                    error_location = statistician.data[statistician.current_progress - 1]
                self.logger.warning(f"统计失败 错误位置:{error_location}\n"
                                    f"失败原因:\n"
                                    f"{str(statistics_error)}")
                ui_signals.callErrorBox.emit(statistics_error)

            finally:
                self.ui.statisticsRunButton.setEnabled(True)

        try:
            # 读取参数
            self.read_file_path()
            args = get_args_ui()

            # 根据参数生成文件管道和统计器
            statistician: UsersStatistician | CommentsStatistician
            if args["type"] == "用户":
                pipe = UsrFilePipe(self.statistics_in_path, "r")
                pipe_stop = SwdFilePipe("stopwords.json", "r")
                users = pipe.load()
                statistician = UsersStatistician(users,
                                                 progress_signal=ui_signals.updateProgressBar,
                                                 maximum_signal=ui_signals.setProgressBar)
            elif args["type"] == "评论":
                pipe = CmtFilePipe(self.statistics_in_path, "r")
                pipe_stop = SwdFilePipe("stopwords.json", "r")
                comments = pipe.load()
                statistician = CommentsStatistician(comments,
                                                    progress_signal=ui_signals.updateProgressBar,
                                                    maximum_signal=ui_signals.setProgressBar)
            else:
                raise FileFormatException("统计类型选择错误")

            self.logger.info(f"统计开始 统计参数:\n"
                             f"统计类型:{args['type']}\n"
                             f"统计属性:{args['property']}\n"
                             f"显示模式:{args['show']}")

            thread = threading.Thread(target=statistics)
            thread.start()
        except AnalyzerException as error:
            call_msg_box(self, str(error))

        else:
            self.ui.statisticsProgress.setValue(0)
            self.ui.statisticsProgress.setMaximum(100)
            self.ui.statisticsRunButton.setEnabled(False)

    def show_statistics_result(self, result: OrderedDict, headers: list[str]):
        self.ui.statisticsTable.setRowCount(len(result))
        self.ui.statisticsTable.setColumnCount(2)
        self.ui.statisticsTable.setHorizontalHeaderLabels(headers)
        self.ui.statisticsTable.setColumnWidth(0, 10)
        self.ui.statisticsTable.setColumnWidth(1, 10)

        for index, (name, count) in enumerate(result.items()):
            self.ui.statisticsTable.setItem(index, 0, QTableWidgetItem(str(name)))
            self.ui.statisticsTable.setItem(index, 1, QTableWidgetItem(str(count)))
        self.ui.statisticsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.statisticsTable.show()

    def show_statistics_property(self):
        statistics_type = self.ui.statisticsTypeBox.currentText()
        if statistics_type == "用户":
            self.ui.statisticsPropertyBox.clear()
            self.ui.statisticsPropertyBox.addItem("性别")
            self.ui.statisticsPropertyBox.addItem("生日")
            self.ui.statisticsPropertyBox.addItem("学校")
            self.ui.statisticsPropertyBox.addItem("专业")
            self.ui.statisticsPropertyBox.addItem("UID位数")
            self.ui.statisticsPropertyBox.addItem("等级")
            self.ui.statisticsPropertyBox.addItem("大会员")
            self.ui.statisticsPropertyBox.addItem("标签")
            self.ui.statisticsPropertyBox.addItem("装扮")
            self.ui.statisticsPropertyBox.addItem("名牌")
            self.ui.statisticsPropertyBox.addItem("关注")
            self.ui.statisticsPropertyBox.addItem("粉丝牌")

        elif statistics_type == "评论":
            self.ui.statisticsPropertyBox.clear()
            self.ui.statisticsPropertyBox.addItem("内容")
            self.ui.statisticsPropertyBox.addItem("表情(评论数)")
            self.ui.statisticsPropertyBox.addItem("表情(个数)")

        else:
            return

    def export_analyze_uidfile(self):
        filepath, filetype = QFileDialog.getSaveFileName(self, filter="json文件(*.json)")
        if filepath == "":
            return
        self.read_file_path()
        uidfile_path = filepath
        pipe_in = CmtFilePipe(self.analyze_in_path, "r")
        pipe_out = UidFilePipe(uidfile_path, "w")

        comments = pipe_in.load()
        uids = convert_comments_to_uids(comments)
        pipe_out.dump(uids)

    def export_statistics_resfile(self):
        if self.statistics_result is None:
            call_msg_box(self, "请先统计才能进行导出")
            return
        self.logger.info("开始保存统计结果")
        filepath, filetype = QFileDialog.getSaveFileName(self, filter="json文件 (*.json)")
        pipe = ResFilePipe(filepath, "w")
        pipe.dump(self.statistics_result)
        self.logger.info(f"保存完毕 保存位置: {filepath}")

    def select_analyze_cmtfile(self):
        self.read_file_path()
        filepath, filetype = QFileDialog.getOpenFileName(self, filter="cmt文件(*.cmt)")
        if os.path.exists(filepath):
            self.analyze_in_path = filepath
        self.show_file_path()

    def select_analyze_usrfile(self):
        self.read_file_path()
        filepath, filetype = QFileDialog.getSaveFileName(self, filter="usr文件(*.usr)")
        self.analyze_out_path = filepath
        self.show_file_path()

    def select_statistics_srcfile(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         filter="usr文件(*.usr);;cmt文件(*.cmt)",
                                                         selectedFilter="usr文件(*.usr)")
        if filepath == "":
            return
        elif os.path.exists(filepath):
            self.statistics_in_path = filepath
        self.show_file_path()

    def read_file_path(self):
        self.analyze_in_path = self.ui.analyzeCmtfileInput.text()
        self.analyze_out_path = self.ui.analyzeUsrfileInput.text()
        self.statistics_in_path = self.ui.statisticsFileInput.text()

    def show_file_path(self):
        self.ui.analyzeCmtfileInput.setText(self.analyze_in_path)
        self.ui.analyzeUsrfileInput.setText(self.analyze_out_path)
        self.ui.statisticsFileInput.setText(self.statistics_in_path)

    def update_progress_bar(self, value: int, bar_name: Literal["下载", "分析", "统计"]):
        progress_bar: QProgressBar = {
            "下载": self.ui.downloadProgress,
            "分析": self.ui.analyzeProgress,
            "统计": self.ui.statisticsProgress
        }[bar_name]
        progress_bar.setValue(value)

    def set_progress_bar(self, maximum: int, bar_name: Literal["下载", "分析", "统计"]):
        progress_bar: QProgressBar = {
            "下载": self.ui.downloadProgress,
            "分析": self.ui.analyzeProgress,
            "统计": self.ui.statisticsProgress
        }[bar_name]
        progress_bar.setMaximum(maximum)

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
        self.revealing: bool = False  # 当前是否以直接显示Cookies

    def bind(self):
        self.ui.confirmButton.accepted.connect(self.confirm_accepted)
        self.ui.confirmButton.rejected.connect(self.confirm_rejected)
        self.ui.credentialScanButton.clicked.connect(self.scan_credential)
        self.ui.credentialImportButton.clicked.connect(self.import_credential)
        self.ui.credentialExportButton.clicked.connect(self.export_credential)
        self.ui.credentialRevealButton.clicked.connect(self.reveal_credential)
        self.ui.resultPathButton.clicked.connect(self.select_result_path)

    def show_config(self):
        # 在UI上显示设置
        self.ui.resultPathInput.setText(self.configer.config.result_path)

        # 在UI上显示凭证
        credential = self.configer.credential
        if credential.sessdata is not None:
            self.ui.credentialSessdataInput.setText(credential.sessdata)
        if credential.bili_jct is not None:
            self.ui.credentialBilijctInput.setText(credential.bili_jct)
        if credential.buvid3 is not None:
            self.ui.credentialBuvid3Input.setText(credential.buvid3)
        if credential.dedeuserid is not None:
            self.ui.credentialDedeuseridInput.setText(credential.dedeuserid)

    def read_config(self):
        # 从UI上读取设置
        self.configer.config = Config(result_path=self.ui.resultPathInput.text())

        sessdata = self.ui.credentialSessdataInput.text() \
            if self.ui.credentialSessdataInput.text() != "" else None
        bili_jct = self.ui.credentialBilijctInput.text() \
            if self.ui.credentialBilijctInput.text() != "" else None
        buvid3 = self.ui.credentialBuvid3Input.text() if self.ui.credentialBuvid3Input.text() != "" else None
        dedeuserid = self.ui.credentialDedeuseridInput.text() \
            if self.ui.credentialDedeuseridInput.text() != "" else None

        # 从UI上读取凭证
        self.configer.credential = Credential(
            sessdata=sessdata,
            bili_jct=bili_jct,
            buvid3=buvid3,
            dedeuserid=dedeuserid
        )

    def confirm_accepted(self):
        self.read_config()
        self.main_window.logger.debug(f"当前设置:\n"
                                      f"{str(self.configer)}")
        self.configer.dump_to_file()
        self.close()

    def confirm_rejected(self):
        self.close()

    def scan_credential(self):
        self.configer.scan_credential()

        credential = self.configer.credential
        if credential.sessdata is not None:
            self.ui.credentialSessdataInput.setText(credential.sessdata)
        if credential.bili_jct is not None:
            self.ui.credentialBilijctInput.setText(credential.bili_jct)
        if credential.buvid3 is not None:
            self.ui.credentialBuvid3Input.setText(credential.buvid3)
        if credential.dedeuserid is not None:
            self.ui.credentialDedeuseridInput.setText(credential.dedeuserid)

    def import_credential(self):
        try:
            filepath, filetype = QFileDialog.getOpenFileName(self)
            if os.path.exists(filepath):
                self.configer.import_credential(filepath)
            elif filepath == "":
                return
        except FileNotFoundError:
            call_msg_box(self, "文件不存在")
        except (TypeError | ValueError):
            call_msg_box(self, "文件格式错误")
        self.show_config()

    def export_credential(self):
        filepath, filetype = QFileDialog.getSaveFileName(self)
        self.read_config()
        if filepath == "":
            return
        else:
            self.configer.export_credential(filepath)

    def reveal_credential(self):
        self.revealing = not self.revealing
        if self.revealing:
            self.ui.credentialSessdataInput.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.credentialBilijctInput.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.credentialBuvid3Input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.credentialDedeuseridInput.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.credentialSessdataInput.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.credentialBilijctInput.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.credentialBuvid3Input.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.credentialDedeuseridInput.setEchoMode(QLineEdit.EchoMode.Password)

    def select_result_path(self):
        filepath = QFileDialog.getExistingDirectory(self)
        if filepath != "":
            self.configer.config.result_path = filepath
        self.show_config()


class AboutWindow(QWidget):
    def __init__(self, main_window: MainWindow):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutWindow()
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
        QMessageBox.information(parent, "提示", content, QMessageBox.StandardButton.Ok)
    elif level == "warning":
        QMessageBox.warning(parent, "警告", content, QMessageBox.StandardButton.Ok)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
