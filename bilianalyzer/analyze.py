import abc
import json
import time
from collections import OrderedDict
from typing import Literal

from PySide6.QtCore import Signal
from bilibili_api import sync, Credential
from bilibili_api.user import User

from download import RawData


class Analysis(metaclass=abc.ABCMeta):
    """
    分析结果处理相关操作

    Attributes:
        user    (User)  : 分析所属用户
    """

    def __init__(self, user: User, raw: RawData):
        self.user = user
        self.parse(raw)

    @abc.abstractmethod
    def parse(self, raw: RawData):
        """
        子类必须实现解析RawData的方法
        Args:
            raw (RawData)   : API返回结果
        """
        raise NotImplementedError("子类必须实现解析raw的方法")


class FanMedal(Analysis):
    """
    用户粉丝牌分析结果
    """

    def __init__(self, user: User, raw: RawData):
        self.result: OrderedDict = OrderedDict()
        super(FanMedal, self).__init__(user, raw)

    def parse(self, raw: RawData):
        """
        解析为顺序映射并按等级进行排序
        Args:
            raw     (RawData)   : API返回结果
        """
        for each in raw["list"]:
            self.result[each["target_name"]] = each["medal_info"]["level"]
        self.result = OrderedDict(sorted(self.result.items(), key=lambda item: item[1], reverse=True))


class Followings(Analysis):
    """
    用户关注分析结果
    """

    def __init__(self, user: User, raw: RawData):
        self.result: list = []
        super(Followings, self).__init__(user, raw)

    def parse(self, raw: RawData):
        """
        解析为UID列表
        Args:
            raw     (RawData)   : API返回结果
        """
        uid: int
        for uid in raw:
            self.result.append(uid)


class UserAnalyzer:
    """
    Attributes:
        users               (list[User] | None)         : 用户列表
        credential          (Credential | None)         : 凭据. Defaults to None.
        current_progress    (int)                       : 当前进度
        maximum_progress    (int)                       : 最大进度
        progress_signal     (Signal | None, optional)   : 更新进度条的信号
    """

    def __init__(self,
                 users: list[User] | None = None,
                 credential: Credential | None = None,
                 progress_signal: Signal | None = None):
        """

        Args:
            users           (list[User] | None)         : 用户列表. None表示稍后传入
            credential      (Credential | None)         : 凭据. Defaults to None.
            progress_signal (Signal | None, optional)   : 更新进度条的信号
        """
        self.users: list[User] = []
        if users is not None:
            self.users = users
        self.credential = credential
        if self.credential is not None:
            for user in self.users:
                user.credential = self.credential

        self.current_progress: int = 0
        self.maximum_progress: int = len(self.users)
        self.progress_signal = progress_signal

    def import_from_comments(self, comment_file: str):
        with open(comment_file, "r", encoding="utf-8") as f:
            comments = json.load(f)

        for comment in comments:
            user = User(comment["user"])
            if not self.check_in_users(user):
                self.users.append(user)
        if self.credential is not None:
            for user in self.users:
                user.credential = self.credential
        self.maximum_progress: int = len(self.users)

    def check_in_users(self, user):
        for each in self.users:
            if user.get_uid() == each.get_uid():
                return True
        return False

    @staticmethod
    def get_top_result(result: OrderedDict, n: int):
        result = OrderedDict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        return OrderedDict(list(result.items())[:n]) if n < len(result) else result

    def analyze(self, analyze_mode: Literal["FanMedal", "Followings"]):
        result = OrderedDict()
        for index, user in enumerate(self.users):

            if analyze_mode == "FanMedal":
                coroutine = user.get_user_medal()
                raw: RawData = sync(coroutine)
                for key in FanMedal(user, raw).result:
                    result.setdefault(key, 0)
                    result[key] += 1
            elif analyze_mode == "Followings":
                coroutine = user.get_all_followings()
                raw: RawData = sync(coroutine)
                time.sleep(1)
                for key in Followings(user, raw).result:
                    result.setdefault(key, 0)
                    result[key] += 1

            if self.progress_signal is not None:
                self.current_progress = index + 1
                self.progress_signal.emit(self.current_progress)
            time.sleep(1)

        return result
