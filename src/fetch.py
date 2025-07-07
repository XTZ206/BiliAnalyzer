import json
import time
import os
from bilibili_api import Credential, bvid2aid, sync
from bilibili_api.comment import CommentResourceType, get_comments

from utils import *


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
    uids: dict[int, Member] = {}
    for reply in replies:
        member = reply.get("member", {})
        uid: int = member.get("mid")
        if uid is None:
            continue
        if uid not in uids:
            uids[uid] = member
            members.append(member)
        else:
            # Update existing member with new information
            existing_member = uids[uid]
            for key, value in member.items():
                if key not in existing_member or not existing_member[key]:
                    existing_member[key] = value
            uids[uid] = existing_member
    return members


def load_replies(filepath: FilePath) -> list[Reply]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)


def load_members(filepath: FilePath) -> list[Member]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)


def save_replies(replies: Collection[Reply], filepath: FilePath) -> None:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(list(replies), f, ensure_ascii=False, indent=4)


def save_members(members: Collection[Member], filepath: FilePath) -> None:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(list(members), f, ensure_ascii=False, indent=4)
