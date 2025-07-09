import json
import os
from bilibili_api import Credential, bvid2aid
from bilibili_api.comment import CommentResourceType, get_comments
import asyncio
import random
from utils import *

async def fetch_page(bvid: str, index: int, credential: Optional[Credential] = None) -> list[Reply]:
    page: Page = await get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, index,credential=credential)
    page_reply: list[Reply] = []
    
    reply: Reply
    for reply in page.get("replies", []):
        page_reply.append(reply)
        for reply in reply.get("replies", []):
            page_reply.append(reply)
    return page_reply

async def fetch_replies(bvid: str, limit: int = 20, credential: Optional[Credential] = None) -> list[Reply]:
    page: Page = await get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, credential=credential)
    count: int = page.get("page", {}).get("count", 0)
    all_replies: list[Reply] = []
    total_pages:int = (count // 20) + 1
    pages_to_fetch: range = range(1, total_pages + 1) if limit == 0 else range(1, min(total_pages, limit) + 1)
    
    semaphore = asyncio.Semaphore(5)
    
    async def bounded_fetch(page_num):
        async with semaphore:
            await asyncio.sleep(0.5 + random.random())
            return await fetch_page(bvid, page_num, credential)
        
    tasks:list = [bounded_fetch(index) for index in pages_to_fetch]  
    results:list = await asyncio.gather(*tasks)       
    
    all_replies = [reply for page_replies in results for reply in page_replies]
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
