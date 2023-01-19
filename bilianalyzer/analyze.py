import abc
import json
from os import PathLike
from typing import TextIO

from bilibili_api import sync, Credential
from bilibili_api.user import User

from download import RawData


class Analysis(metaclass=abc.ABCMeta):
    def __init__(self, user: User, raw: RawData):
        self.user = user
        self.parse(raw)

    @abc.abstractmethod
    def parse(self, raw: RawData):
        raise NotImplementedError("子类必须实现解析raw的方法")


class FanMedal(Analysis):
    """
    粉丝牌用户结果
    """

    def __init__(self, user: User, raw: RawData):
        self.medals: dict = {}
        super(FanMedal, self).__init__(user, raw)

    def parse(self, raw: RawData):
        for each_medal in raw["list"]:
            self.medals[each_medal["target_name"]] = each_medal["medal_info"]["level"]


class Followings(Analysis):
    def __init__(self, user: User, raw: RawData):
        self.followings: list = []
        super(Followings, self).__init__(user, raw)

    def parse(self, raw: RawData):
        for each in raw:
            self.followings.append(User(each))


class UserAnalyzer:
    def __init__(self, users: list[User] | None = None, credential: Credential | None = None):
        self.credential = credential
        self.users: list[User] = []
        if users is not None:
            self.users = []
        for user in self.users:
            user.credential = self.credential
        self.analysis: list[Analysis] = []

    def import_from_comments(self, comment_file: str):
        with open(comment_file, "r", encoding="utf-8") as f:
            comments = json.load(f)
        for comment in comments:
            user = User(comment["user"])
            if not self.check_in_users(user):
                self.users.append(user)
        for user in self.users:
            user.credential = self.credential

    def check_in_users(self, user):
        for each in self.users:
            if user.get_uid() == each.get_uid():
                return True
        return False

    def analyze_users_medal(self):
        for user in self.users:
            coroutine = user.get_user_medal()
            raw: RawData = sync(coroutine)
            self.analysis.append(FanMedal(user, raw))
        return self.analysis

    def analyze_users_following(self):
        for user in self.users:
            coroutine = user.get_all_followings()
            raw: RawData = sync(coroutine)
            self.analysis.append(Followings(user, raw))
        return self.analysis


if __name__ == '__main__':
    uid = 61935349  # 测试用UID

    with open("credential", "r", encoding="utf-8") as f:
        user_analyzer = UserAnalyzer([User(uid)], Credential(**(json.load(f))))
    medals = user_analyzer.analyze_users_medal()
    followings = user_analyzer.analyze_users_following()
