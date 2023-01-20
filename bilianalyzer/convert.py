import json

from bilibili_api import bvid2aid, aid2bvid
from bilibili_api.user import User

from bilianalyzer.exceptions import FileFormatException


def convert_video_id(sid: str) -> str:
    """
    把字符串输入的源ID转换为AV号/BV号
    Args:
        sid     (str)   : 源ID 可能为AV号可能为BV号
    Returns:
        str:    BV号 或 AV号的字符串
    """

    # 如果是BV号
    if sid.startswith("bv") or sid.startswith("BV"):
        try:
            res = str(bvid2aid(sid))
        except IndexError:
            raise ValueError("输入的BV号必须带有BV前缀且有效\n")
        else:
            return res

    elif sid.startswith("av") or sid.isdigit():
        sid = sid.removeprefix("av")
        try:
            res = aid2bvid(int(sid))
            return res
        except ValueError:
            raise ValueError("输入的av号只能带有数字")
    elif sid == "":
        raise ValueError("输入的值不能为空")
    else:
        raise ValueError("输入的值格式错误\nBV号必须带有前缀")


def convert_cmtfile_to_users(cmtfile: str) -> list[User]:
    """

    Args:
        cmtfile     (str)   : 评论文件路径

    Returns:
        list[User]: 转换得到的用户列表 无重复
    """
    with open(cmtfile, "r", encoding="utf-8") as f:
        comments = json.load(f)

    try:
        uids: set[int] = set()
        for comment in comments:
            uids.add(comment["user"])
        return [User(uid) for uid in uids]

    except KeyError:
        raise FileFormatException("文件格式错误")
