from typing import TypeAlias, Sequence

from bilibili_api.comment import CommentResourceType
from bilibili_api.user import User

RawData: TypeAlias = list | dict  # API返回结果


class CommentStorage:
    """
    保存评论相关信息

    Attributes:
        rpid    (int)                           : 评论ID
        oid     (int)                           : 评论所在资源ID
        otype   (CommentResourceType | None)    : 评论所在资源类枚举
        user    (User)                          : 评论用户
        time    (int)                           : 评论发出时间的时间戳
        root    (int)                           : 根评论ID
        parent  (int)                           : 父评论ID
        content (str)                           : 评论内容
        emotes  (list[str])                     : 评论表情
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
            self.otype: CommentResourceType | None = CommentResourceType(raw_data["type"])
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
            self.otype: CommentResourceType | None = CommentResourceType[cmt_file["otype"]]
            self.user: User = User(cmt_file["user"])
            self.time: list[str] = cmt_file["time"]
            self.root: list[str] = cmt_file["root"]
            self.parent: list[str] = cmt_file["parent"]
            self.content: list[str] = cmt_file["content"]
            self.emotes: list[str] = cmt_file["emotes"]
        else:
            self.rpid: int = 0
            self.oid: int = 0
            self.otype: CommentResourceType | None = None
            self.user: User = User(0)
            self.time: int = 0
            self.root: int = 0
            self.parent: int = 0
            self.content: str = ""
            self.emotes: list[str] = []

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

            self.uid: int = 0
            self.name: str = "未知"
            self.sign: str = "未知"
            self.level: str = "未知"
            self.vip: str = "未知"
            self.tags: list[str] = []
            self.pendant: str = "无名牌"
            self.nameplate: str = "无名牌"
            self.sex: str = "保密"
            self.birthday: str = "未知"
            self.school: str = "未知"
            self.profession: str = "未知"
            self.official: dict[str, str] = {"type": "无认证", "title": "", "desc": ""}
            self.followings: list[int] = []
            self.fan_medals: dict[str, int] = {}

            raw_basic_info = raw_data[0]
            raw_followings = raw_data[1]
            raw_fan_medals = raw_data[2]

            # 解析基础用户数据
            self.uid: int = raw_basic_info["mid"]
            self.name: str = raw_basic_info["name"]
            self.sign: str = raw_basic_info["sign"]
            self.level: int = raw_basic_info["level"] + raw_basic_info["is_senior_member"]
            self.vip: str = raw_basic_info["vip"]["label"]["text"] \
                if raw_basic_info["vip"]["status"] == 1 else "普通用户"

            # 解析用户社交数据
            if raw_basic_info["tags"] is not None:
                self.tags = raw_basic_info["tags"]
            if raw_basic_info["pendant"] is not None:
                if raw_basic_info["pendant"]["name"] != "":
                    self.pendant = raw_basic_info["pendant"]["name"]
            if raw_basic_info["nameplate"] is not None:
                if raw_basic_info["nameplate"]["name"] != "":
                    self.nameplate = raw_basic_info["nameplate"]["name"]

            # 解析用户隐私数据
            if raw_basic_info["sex"] is not None:
                self.sex = raw_basic_info["sex"]
            if raw_basic_info["birthday"] is not None:
                self.birthday = raw_basic_info["birthday"]
            if raw_basic_info["school"] is not None:
                if raw_basic_info["school"]["name"] != "":
                    self.school = raw_basic_info["school"]["name"]
            if raw_basic_info["profession"] is not None:
                if raw_basic_info["profession"]["name"] != "":
                    self.profession = raw_basic_info["profession"]["name"]

            # 解析用户认证信息
            official_type = {
                -1: "无认证",
                0: "个人认证",
                1: "机构认证",

            }[raw_basic_info["official"]["type"]]
            official_title = raw_basic_info["official"]["title"]
            official_desc = raw_basic_info["official"]["desc"]
            self.official: dict = {
                "type": official_type,
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
            self.sign: str = usr_file["sign"]
            self.level: str = usr_file["level"]
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
            self.uid: int = 0
            self.name: str = "未知"
            self.sign: str = "未知"
            self.level: str = "未知"
            self.vip: str = "未知"
            self.tags: list[str] = []
            self.pendant: str = "无名牌"
            self.nameplate: str = "无名牌"
            self.sex: str = "保密"
            self.birthday: str = "未知"
            self.school: str = "未知"
            self.profession: str = "未知"
            self.official: dict[str, str] = {"type": "无认证", "title": "", "desc": ""}
            self.followings: list[int] = []
            self.fan_medals: dict[str, int] = {}

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

    def __str__(self):
        return self.uid
