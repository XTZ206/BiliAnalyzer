import json
from typing import TypeAlias, Sequence

from bilibili_api.comment import CommentResourceType
from bilibili_api.user import User

from exceptions import StorageException

RawData: TypeAlias = list | dict  # API返回结果


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

    def __init__(self, *, raw_data: RawData | None = None, cmt_file: dict | None = None):
        """
        从API返回结果/cmt文件读取结果生成储存于内存中的评论数据格式
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
        return [CommentStorage(cmt_file=comment) for comment in self.content]

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


class UserStorage:
    """
    保存用户相关信息

    Attributes:
        uid         (int)           : 用户UID
        name        (str)           : 用户昵称
        sign        (str)           : 用户签名
        level       (int)           : 用户等级. 等于7时表示硬核会员
        vip         (str)           : 用户的大会员类型
        tags        (list[str])     : 用户标签
        pendant     (str)           : 用户挂件
        nameplate   (str)           : 用户名牌
        sex         (str)           : 用户性别
        birthday    (str)           : 用户生日(格式"mm-dd")
        school      (str)           : 用户学校
        profession  (str)           : 用户专业
        official    (dict[str, str]): 用户认证(认证类型, 认证头衔, 认证描述)
    """

    def __init__(self, *, raw_data: Sequence[RawData] | None = None, usr_file: dict | None = None):
        """
        从API返回结果/usr文件读取结果生成储存于内存中的用户数据格式
        Args:
            raw_data    (RawData)   : API返回结果，与usr_file同时传入时覆盖usr_file
            usr_file    (dict)      : .usr文件读取结果，不能与raw_data同时为空
        """
        if raw_data is not None:

            raw_basic_info = raw_data[0]
            raw_followings = raw_data[1]
            raw_fan_medals = raw_data[2]

            # 解析基础用户数据
            self.uid: int = raw_basic_info["mid"]
            self.name: str = raw_basic_info["name"]
            self.sign: str = raw_basic_info["sign"]
            self.level: int = raw_basic_info["level"] + raw_basic_info["is_senior_member"]
            self.vip: str = raw_basic_info["vip"]["label"]["text"] \
                if raw_basic_info["vip"]["status"] != 1 else "普通用户"
            self.tags: list[str] = raw_basic_info["tags"] if raw_basic_info["tags"] is not None else []
            self.pendant: str = raw_basic_info["pendant"]["name"]
            self.nameplate: str = raw_basic_info["nameplate"]["name"]
            self.sex = raw_basic_info["sex"]
            self.birthday = raw_basic_info["birthday"]
            self.school = raw_basic_info["school"]["name"]
            self.profession = raw_basic_info["school"]["name"]

            # 解析用户认证信息
            official_role = {
                -1: "无认证",
                0: "个人认证",
                1: "机构认证",

            }[raw_basic_info["official"]["role"]]
            official_title = raw_basic_info["official"]["title"]
            official_desc = raw_basic_info["official"]["desc"]
            self.official: dict = {
                "type": official_role,
                "title": official_title,
                "desc": official_desc
            }

            # 解析关注数据
            self.followings: list[int] = list(raw_followings)

            # 解析粉丝牌数据
            self.fan_medals: dict[int, int] = {}
            for each in raw_fan_medals["list"]:
                medal_id = each["medal_info"]["target_id"]
                medal_level = each["medal_info"]["level"]
                self.fan_medals[medal_id] = medal_level

        elif usr_file is not None:
            self.uid: int = usr_file["uid"]
            self.name: str = usr_file["name"]
            self.sign: str = usr_file["level"]
            self.vip: str = usr_file["vip"]
            self.tags: list[str] = usr_file["tags"]
            self.pendant: str = usr_file["pendant"]
            self.nameplate: str = usr_file["nameplate"]
            self.sex: str = usr_file["sex"]
            self.birthday: str = usr_file["birthday"]
            self.school: str = usr_file["school"]
            self.profession: str = usr_file["profession"]
            self.official: dict[str, str] = usr_file["official"]
            self.followings: list[int] = usr_file["followings"]
            self.fan_medals: dict[str, int] = usr_file["fan_medals"]
        else:
            raise StorageException("用户存储时传入参数不能同时为空")

    def __eq__(self, other):
        """
        根据uid判断两条UserStorage是否相同
        """
        if type(other) == CommentStorage:
            return self.uid == other.uid
        else:
            return False

    def __hash__(self):
        return hash(self.uid)


class UserFileInterface:
    """
    用户文件处理相关操作
    """

    def __init__(self, filepath: str = ""):
        self.filepath = filepath
        self.content = None

    def load(self) -> list[UserStorage]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        return [UserStorage(usr_file=user) for user in self.content]

    def dump(self, users: list[UserStorage]):
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
