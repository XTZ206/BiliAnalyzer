from typing import List, Tuple, Optional, Literal


class User:
    __slots__ = ["id", "name", "sex", "avatar", "level", "vip", "verify", "sailings"]

    def __init__(self):
        self.id: int = -1
        self.name: str = ""
        self.sex: Literal["男", "女", "保密"] = "保密"
        self.avatar: str = ""
        self.level: int = -1
        self.vip: str = ""
        self.verify: Tuple[str, Optional[str]] = "无认证", None
        self.sailings: Optional[List[str]] = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: "User"):
        return self.id == other.id

class Comment:
    __slots__ = ["id", "send_time", "uid", "message", "emote"]

    def __init__(self):
        self.id: int = -1
        self.send_time: int = -1
        self.uid: int = -1
        self.message: str = ""
        self.emote: Optional[List[str]] = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: "Comment"):
        return self.id == other.id