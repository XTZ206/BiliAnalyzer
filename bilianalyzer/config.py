import json
import os

from bilibili_api import Credential
from bilibili_api.login import login_with_qrcode

from bilianalyzer.pipes import CdtFilePipe


class Config:
    """
    设置处理 相关操作

    Attributes:
        result_path         (str)       : 结果保存路径.
    """

    def __init__(self, result_path: str | None = None):
        """
        Args:
            result_path     (str | None, optional)  : 结果保存路径.Defaults to None.

        """
        self.result_path = result_path if result_path is not None else ""


class Configer:
    """
    设置与凭证 读取存储相关操作

    Attribute:
        config      (Config)                        : 设置.
        credential  (Credential | None, optional)   : 凭据. Defaults to None.
    """

    def __init__(self):
        # 如果配置文件不存在则使用默认设置
        self.config: Config | None = None
        self.credential: Credential | None = None
        self.load_from_file()
        self.dump_to_file()

    def load_from_file(self):
        # 读取设置文件
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                self.config = Config(**(json.load(f)))
        else:
            self.config = Config()

        # 读取凭证文件
        if os.path.exists("credential"):
            self.import_credential("credential")
        else:
            self.credential = Credential()

    def dump_to_file(self):
        # 写入设置文件
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({
                "result_path": self.config.result_path
            }, f, indent=4, ensure_ascii=False)

        # 写入凭证文件
        self.export_credential("credential")

    def import_credential(self, filepath):
        pipe = CdtFilePipe(filepath, "r")
        self.credential: Credential = Credential(**pipe.load())

    def export_credential(self, filepath):
        content = {
            "sessdata": self.credential.sessdata,
            "bili_jct": self.credential.bili_jct,
            "buvid3": self.credential.buvid3,
            "dedeuserid": self.credential.dedeuserid
        }

        pipe = CdtFilePipe(filepath, "w")
        pipe.dump(content)

    # TODO: 自定义扫码窗口
    def scan_credential(self):
        self.credential = login_with_qrcode()

    def __str__(self):
        return json.dumps({
            "result_path": self.config.result_path,
            "sessdata": self.credential.sessdata,
            "bili_jct": self.credential.bili_jct,
            "buvid3": self.credential.buvid3,
            "dedeuserid": self.credential.dedeuserid
        }, indent=4)
