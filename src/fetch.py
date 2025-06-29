import json
import time
import os
from os import PathLike
from typing import Optional, Any, Collection

from bilibili_api import Credential, bvid2aid, sync
from bilibili_api.comment import CommentResourceType, get_comments

Member = dict[str, Any]
Reply = dict[str, Any]
Page = dict[str, Any]


def fetch_replies(bvid: str, limit: int = 20, credential: Optional[Credential] = None) -> list[Reply]:
    page: Page = sync(get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, credential=credential))
    count: int = page.get("page", {}).get("count", 0)
    index: int = 1
    replies: list[Reply] = []

    for reply in page.get("replies", []):
        replies.append(reply)
        for reply in reply.get("replies", []):
            replies.append(reply)

    while limit == 0 or index < limit:
        if len(replies) >= count or page.get("replies") == []:
            break
        index += 1
        page: Page = sync(get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, index, credential=credential))
        time.sleep(1)
        for reply in page.get("replies", []):
            replies.append(reply)
            for reply in reply.get("replies", []):
                replies.append(reply)

    return replies


def fetch_members(replies: Collection[Reply]) -> list[Member]:
    members: list[Member] = []
    mids: set[int] = set()
    for reply in replies:
        member = reply.get("member", {})
        mid = member.get("mid")
        if mid is not None and mid not in mids:
            mids.add(mid)
            members.append(member)
    return members


def load_replies(filepath: PathLike) -> list[Reply]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)


def load_members(filepath: PathLike) -> list[Member]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)


def store_replies(replies: Collection[Reply], filepath: PathLike) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(list(replies), f, ensure_ascii=False, indent=4)


def store_members(members: Collection[Member], filepath: PathLike) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(list(members), f, ensure_ascii=False, indent=4)
