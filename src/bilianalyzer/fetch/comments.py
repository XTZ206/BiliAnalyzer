import asyncio
import math
import json
import os
import random
from typing import Coroutine
from bilibili_api import Credential, bvid2aid
from bilibili_api.video import Video
from bilibili_api.comment import CommentResourceType, get_comments

from ..utils import *

COMMENTS_PER_PAGE = 20


async def fetch_page_replies(bvid: str, index: int, credential: Optional[Credential] = None) -> list[Reply]:
    page: Page = await get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, index, credential=credential)
    return flatten_replies(page)


def flatten_replies(page: Page) -> list[Reply]:
    page_replies: list[Reply] = []

    reply: Reply
    for reply in page.get("replies", []):
        page_replies.append(reply)
        for reply in reply.get("replies", []):
            page_replies.append(reply)
    return page_replies


async def fetch_replies(bvid: str, limit: int = 20, credential: Optional[Credential] = None) -> list[Reply]:
    page: Page = await get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, credential=credential)
    reply_count: int = page.get("page", {}).get("count", 0)
    all_replies: list[Reply] = []
    page_count: int = math.ceil(reply_count / COMMENTS_PER_PAGE)
    page_index_range: Collection[int] = range(2, page_count + 1) if limit == 0 else range(2, min(page_count, limit) + 1)
    # TODO: early termination if empty page is fetched

    all_replies.extend(flatten_replies(page))

    semaphore = asyncio.Semaphore(5)

    async def bounded_fetch(page_index: int) -> list[Reply]:
        async with semaphore:
            await asyncio.sleep(0.5 + random.random())
            return await fetch_page_replies(bvid, page_index, credential)

    tasks: list[Coroutine] = [bounded_fetch(index) for index in page_index_range]

    pages_replies: list[list[Reply]] = await asyncio.gather(*tasks)

    for page_replies in pages_replies:
        all_replies.extend(page_replies)
    return all_replies


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


async def fetch_video_info(bvid: str, credential: Optional[Credential] = None) -> list[VideoInfo]:
    video_info: VideoInfo = await Video(bvid, credential=credential).get_info()
    return [video_info]


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


def load_video_info(filepath: FilePath) -> list[VideoInfo]:
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


def save_video_info(video_info: Collection[VideoInfo], filepath: FilePath) -> None:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(list(video_info), f, ensure_ascii=False, indent=4)
