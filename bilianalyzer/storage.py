import json
from typing import NewType

from bilibili_api.comment import CommentResourceType
from bilibili_api.user import User

from exceptions import StorageException

RawData = NewType("RawData", dict)  # API返回结果


class CommentStorage:
    """
    保存评论相关信息

    Attributes:
        rpid    (int)                   : 评论ID
        oid     (int)                   : 评论所在资源ID
        otype   (CommentResourceType)   : 评论所在资源类枚举
        user    (User)                  : 评论用户
        time    (int)                   : 评论发出时间的时间戳
        root    (int)                   : 根评论ID
        parent  (int)                   : 父评论ID
        content (str)                   : 评论内容
        emotes  (list[str])             : 评论表情
    """

    def __init__(self, raw_data: RawData | None = None, cmt_file: dict | None = None):
        """
        从API返回结果/cmt文件读取结果生成储存于内存中的评论格式
        Args:
            raw_data    (RawData)   : API返回结果，与cmt_file同时传入时覆盖cmt_file
            cmt_file    (dict)      : .cmt文件读取结果，不能与raw_data同时为空
        """
        if raw_data is not None:
            self.rpid: int = raw_data["rpid"]
            self.oid: int = raw_data["oid"]
            self.otype: CommentResourceType = CommentResourceType(raw_data["type"])
            self.user: User = User(raw_data["mid"])
            self.time: int = raw_data["ctime"]
            self.root: int = raw_data["root"]
            self.parent: int = raw_data["parent"]
            self.content: str = raw_data["content"]["message"]
            self.emotes: list[str] = []
            if "emote" in raw_data["content"]:
                self.emotes = list(raw_data["content"]["emote"].keys())
        elif cmt_file is not None:
            self.rpid: int = cmt_file["rpid"]
            self.oid: int = cmt_file["oid"]
            self.otype: CommentResourceType = CommentResourceType[cmt_file["otype"]]
            self.user: User = User(cmt_file["user"])
            self.time = cmt_file["time"]
            self.root = cmt_file["root"]
            self.parent = cmt_file["parent"]
            self.content = cmt_file["content"]
            self.emotes = cmt_file["emotes"]
        else:
            raise StorageException("评论存储时传入参数不能同时为空")

    def __eq__(self, other):
        """
        根据rpid判断两条Comment是否相同
        """
        if type(other) == CommentStorage:
            return self.rpid == other.rpid
        else:
            return False

    def __hash__(self):
        return hash(self.rpid)


class CommentFileInterface:
    """
    评论文件处理相关操作
    """

    def __init__(self, filepath: str = ""):
        self.filepath = filepath
        self.content = None

    def load(self) -> list[CommentStorage]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return [self.content]

    def dump(self, comments: list[CommentStorage]):
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
