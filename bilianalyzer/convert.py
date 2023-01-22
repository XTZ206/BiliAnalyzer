from bilibili_api import bvid2aid, aid2bvid

from bilianalyzer.storage import CommentStorage


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


def convert_comments_to_uids(comments: list[CommentStorage]) -> list[int]:
    """
    从评论列表中提取用户列表
    Args:
        comments    (list[CommentStorage])   : 评论列表

    Returns:
        list[int]: 转换得到的用户列表 无重复
    """
    uids = set()
    for comment in comments:
        uids.add(comment.user.get_uid())
    return list(uids)
