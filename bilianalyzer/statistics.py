import time
from collections import OrderedDict
from enum import Enum

from PySide6.QtCore import Signal
from bilibili_api import sync
from bilibili_api.user import User

from storage import UserStorage


class StatisticsMode(Enum):
    UID = 1
    LEVEL = 2
    VIP = 3
    TAGS = 4
    PENDANT = 5
    NAMEPLATE = 6
    SEX = 7
    BIRTHDAY = 8
    SCHOOL = 9
    PROFESSION = 10
    FOLLOWING = 11
    FAN_MEDALS = 12


class Statistician:
    def __init__(self, users: list[UserStorage],
                 progress_signal: Signal | None,
                 maximum_signal: Signal | None):

        self.users = users
        self.current_progress = 0
        self.maximum_progress = 0
        self.progress_signal = progress_signal
        self.maximum_signal = maximum_signal

    def statistics(self, mode: StatisticsMode,
                   tops: int = 0,
                   output_name: bool = True) \
            -> OrderedDict[str | int, int]:
        results = OrderedDict()

        match mode:

            case StatisticsMode.UID:
                for user in self.users:
                    uid_len = len(str(user.uid))
                    results.setdefault(uid_len, 0)
                    results[uid_len] += 1

            case StatisticsMode.LEVEL:
                for user in self.users:
                    results.setdefault(user.level, 0)
                    results[user.level] += 1

            case StatisticsMode.VIP:
                for user in self.users:
                    results.setdefault(user.vip, 0)
                    results[user.vip] += 1

            case StatisticsMode.TAGS:
                for user in self.users:
                    for tag in user.tags:
                        results.setdefault(tag, 0)
                        results[tag] += 1

            case StatisticsMode.PENDANT:
                for user in self.users:
                    results.setdefault(user.pendant, 0)
                    results[user.pendant] += 1

            case StatisticsMode.NAMEPLATE:
                for user in self.users:
                    results.setdefault(user.nameplate, 0)
                    results[user.nameplate] += 1

            case StatisticsMode.SEX:
                for user in self.users:
                    results.setdefault(user.sex, 0)
                    results[user.sex] += 1
            case StatisticsMode.BIRTHDAY:
                for user in self.users:
                    results.setdefault(user.birthday, 0)
                    results[user.birthday] += 1
            case StatisticsMode.SCHOOL:
                for user in self.users:
                    results.setdefault(user.school, 0)
                    results[user.school] += 1
            case StatisticsMode.PROFESSION:
                for user in self.users:
                    results.setdefault(user.profession, 0)
                    results[user.profession] += 1

            case StatisticsMode.FOLLOWING:
                for user in self.users:
                    for following in user.followings:
                        results.setdefault(following, 0)
                        results[following] += 1

            case StatisticsMode.FAN_MEDALS:
                for user in self.users:
                    for fan_medal in user.fan_medals:
                        results.setdefault(fan_medal, 0)
                        results[fan_medal] += 1

            case default:
                raise ValueError(f"统计模式错误, 不存在的模式{default}")

        results = OrderedDict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        if tops:
            results = OrderedDict(list(results.items())[:tops]) if 0 < tops < len(results) else results

        if output_name and \
                mode in (StatisticsMode.FOLLOWING, StatisticsMode.FAN_MEDALS):
            uids = list(results.keys())
            names = self.get_users_name(uids)
            results = OrderedDict([(names[i], results[uids[i]]) for i in range(len(names))])
        return results

    def get_users_name(self, uids: list[int]):
        self.maximum_progress = len(uids)
        if self.maximum_signal is not None:
            self.maximum_signal.emit(self.maximum_progress, "统计")

        names: list[str] = []
        for index, uid in enumerate(uids):
            self.current_progress = index + 1
            user = User(uid)
            coroutine = user.get_user_info()
            raw = sync(coroutine)
            name = raw["name"]
            names.append(name)

            if self.progress_signal is not None:
                self.progress_signal.emit(self.current_progress, "统计")
            time.sleep(1)
        return names
