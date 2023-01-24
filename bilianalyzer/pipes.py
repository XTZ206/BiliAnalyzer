import abc
import json
import os
from collections import OrderedDict
from typing import Literal

from bilianalyzer.exceptions import FileNotSelectedException, FileModeException, FileFormatException
from bilianalyzer.storage import CommentStorage, UserStorage


class FilePipe(metaclass=abc.ABCMeta):
    """
    文件处理相关操作
    """

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        self.filepath = filepath
        self.mode = mode
        if self.mode == "r" and not os.path.exists(self.filepath):
            raise FileNotSelectedException("未指定文件")
        self.content = None

    @abc.abstractmethod
    def load(self):
        raise NotImplementedError("子类必须实现load方法")

    @abc.abstractmethod
    def dump(self, data) -> None:
        raise NotImplementedError("子类必须实现dump方法")


class CmtFilePipe(FilePipe):
    """
    评论文件处理相关操作
    """

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        super().__init__(filepath, mode)
        if os.path.splitext(self.filepath)[1] != ".cmt":
            raise FileFormatException("只能打开cmt文件")

    def load(self) -> list[CommentStorage]:
        if self.mode != "r":
            raise FileModeException("只能以读取模式读取文件")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return [CommentStorage(cmt_file=comment) for comment in self.content]

    def dump(self, comments: list[CommentStorage]):
        if self.mode != "w":
            raise FileModeException("只能以写入模式写入文件")
        self.content = [
            {
                "rpid": comment.rpid,
                "oid": comment.oid,
                "otype": comment.otype.name,
                "user": comment.user.get_uid(),
                "time": comment.time,
                "root": comment.root,
                "parent": comment.parent,
                "content": comment.content,
                "emotes": comment.emotes
            }
            for comment in comments]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=4, ensure_ascii=False)


class UidFilePipe(FilePipe):
    """UID文件处理相关操作"""

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        super().__init__(filepath, mode)
        if os.path.splitext(self.filepath)[1] != ".json":
            raise FileFormatException("只能打开json文件")

    def load(self) -> list[int]:
        if self.mode != "r":
            raise FileModeException("只能以读取模式读取文件")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return self.content

    def dump(self, uids: list[int]):
        if self.mode != "w":
            raise FileModeException("只能以写入模式写入文件")
        self.content = uids
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=4, ensure_ascii=False)


class UsrFilePipe(FilePipe):
    """
    用户文件处理相关操作
    """

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        super().__init__(filepath, mode)
        if os.path.splitext(self.filepath)[1] != ".usr":
            raise FileFormatException("只能打开usr文件")

    def load(self) -> list[UserStorage]:
        if self.mode != "r":
            raise FileModeException("只能以读取模式读取文件")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return [UserStorage(usr_file=user) for user in self.content]

    def dump(self, users: list[UserStorage]):
        if self.mode != "w":
            raise FileModeException("只能以写入模式写入文件")
        self.content = [
            {
                "uid": user.uid,
                "name": user.name,
                "sign": user.sign,
                "level": user.level,
                "vip": user.vip,
                "tags": user.tags,
                "pendant": user.pendant,
                "nameplate": user.nameplate,
                "sex": user.sex,
                "birthday": user.birthday,
                "school": user.school,
                "profession": user.profession,
                "official": user.official,
                "followings": user.followings,
                "fan_medals": user.fan_medals
            }
            for user in users]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=4, ensure_ascii=False)


class ResFilePipe(FilePipe):
    """
    结果文件处理相关操作
    """

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        super().__init__(filepath, mode)
        if os.path.splitext(self.filepath)[1] != ".json":
            raise FileFormatException("只能打开json文件")

    def load(self) -> OrderedDict[str, int]:
        if self.mode != "r":
            raise FileModeException("只能以读取模式读取文件")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return OrderedDict(self.content)

    def dump(self, results: OrderedDict[str, int]):
        if self.mode != "w":
            raise FileModeException("只能以写入模式写入文件")
        self.content = results
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=4, ensure_ascii=False)


class SwdFilePipe(FilePipe):
    """
    停用词文件处理相关操作
    """

    def __init__(self, filepath: str, mode: Literal["r", "w"]):
        super().__init__(filepath, mode)
        if os.path.splitext(self.filepath)[1] != ".json":
            raise FileFormatException("只能打开json文件")

    def load(self) -> list[str]:
        if self.mode != "r":
            raise FileModeException("只能以读取模式读取文件")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return self.content

    def dump(self, stopwords: list[str]):
        if self.mode != "w":
            raise FileModeException("只能以写入模式写入文件")
        self.content = stopwords
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=4, ensure_ascii=False)
