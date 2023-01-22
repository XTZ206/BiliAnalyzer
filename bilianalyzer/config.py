import json
import os

from bilibili_api import Credential
from bilibili_api.login import login_with_qrcode

from exceptions import FileNotSelectedException


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
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                self.config = Config(**(json.load(f)))
        else:
            self.config = Config()

        if os.path.exists("credential"):
            with open("credential", "r", encoding="utf-8") as f:
                self.credential = Credential(**(json.load(f)))
        else:
            self.credential = Credential()

    def dump_to_file(self):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({
                "result_path": self.config.result_path
            }, f, indent=4, ensure_ascii=False)
        with open("credential", "w", encoding="utf-8") as f:
            json.dump({
                "sessdata": self.credential.sessdata,
                "bili_jct": self.credential.bili_jct,
                "buvid3": self.credential.buvid3
            }, f, indent=4, ensure_ascii=False)

    def import_credential(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            self.credential: Credential = Credential(**(json.load(f)))

    def export_credential(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "sessdata": self.credential.sessdata,
                "bili_jct": self.credential.bili_jct,
                "buvid3": self.credential.buvid3
            }, f, indent=4, ensure_ascii=False)

    # TODO: 自定义扫码窗口
    def scan_credential(self):
        self.credential = login_with_qrcode()

    def check_download_path(self):
        if not os.path.exists(self.config.result_path):
            raise FileNotSelectedException("未指定下载路径")

    def __str__(self):
        return json.dumps({
            "result_path": self.config.result_path,
            "sessdata": self.credential.sessdata,
            "bili_jct": self.credential.bili_jct,
            "buvid3": self.credential.buvid3
        }, indent=4)
