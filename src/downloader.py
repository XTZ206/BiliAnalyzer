import time
from typing import Optional, Sequence, List, Tuple, Dict, NewType

import bilibili_api
import bilibili_api.comment

from data import Comment, User
from progress import Progress

Page = NewType("Page", Dict[str, Dict])
Reply = NewType("Reply", Dict[str, Dict])
DUPLICATE_KEYS = ("config", "control", "folder", "hots", "upper", "top")
class Processor(Progress):
    def __init__(self):
        super().__init__({"running": "Processing", "finished": "Processed"})

    def pages_to_data(self, pages: List[Page]):
        replies: List[Reply] = self.pages_to_replies(pages)
        self.progress_counter.set_progress_total(len(replies))

        comments = []
        users = []
        for reply in replies:
            comment: Comment = self.reply_to_comment(reply)
            user: User = self.reply_to_user(reply)
            comments.append(comment)
            if user not in users:
                users.append(user)
            self.progress_counter.inc_progress()

        return comments, users

    @staticmethod
    def pages_to_replies(pages: List[Page]) -> List[Reply]:
        replies: List[Reply] = []
        for page in pages:
            for reply in page["replies"]:
                replies.append(reply)
                for sub_reply in reply["replies"]:
                    replies.append(sub_reply)
        return replies

    def reply_to_user(self, reply: Reply) -> User:
        user = User()
        user.id = reply["member"]["mid"]
        user.name = reply["member"]["uname"]
        user.sex = reply["member"]["sex"]
        user.avatar = reply["member"]["avatar"]
        user.level, user.vip = self.get_vip_info(reply["member"]["vip"], reply["member"]["level_info"])
        user.verify = self.get_verify_info(reply["member"]["official_verify"])
        user.sailings = self.get_sailing_info(reply["member"]["user_sailing"])
        return user

    @staticmethod
    def get_vip_info(raw_vip_info, raw_level_info):
        level = raw_level_info["current_level"]
        vip = raw_vip_info["vipType"]
        vip_label = raw_vip_info["label"]["text"]

        # 若当前时间在过期时间后则大会员过期并标记为非大会员
        if raw_vip_info["vipDueDate"] <= int(time.time() * 1000):
            vip = 0

        if vip == 0 and level > 0:
            vip_label = "正式会员"
        elif vip == 0 and level == 0:
            vip_label = "游客"
        if vip_label == "":
            vip_label = "特殊会员"

        return level, vip_label

    @staticmethod
    def get_verify_info(raw_verify_info) -> Tuple[str, Optional[str]]:
        verify_type, verify_desc = "无认证", None

        if raw_verify_info["type"] != -1:
            verify_desc = raw_verify_info["desc"]

            if raw_verify_info["type"] == 0:
                verify_type = "个人认证"
            elif raw_verify_info["type"] == 1:
                verify_type = "组织认证"
            else:
                verify_type = "特殊认证"

        return verify_type, verify_desc

    @staticmethod
    def get_sailing_info(raw_sailings_info):
        if raw_sailings_info is None:
            return None
        sailings = set()
        for each_sailing in raw_sailings_info:
            if raw_sailings_info[each_sailing] is not None:
                sailings.add(raw_sailings_info[each_sailing]["name"])
        if sailings:
            return list(sailings)
        else:
            return None


    def reply_to_comment(self, raw_comment) -> Comment:
        comment: Comment = Comment()
        comment.id = raw_comment["rpid"]
        comment.send_time = raw_comment["ctime"]
        comment.message = raw_comment["content"]["message"]
        comment.uid = raw_comment["member"]["mid"]
        comment.emote = self.get_emote_info(raw_comment["content"])

        return comment

    @staticmethod
    def get_emote_info(raw_content_info):
        if "emote" in raw_content_info:
            emotes = []
            for each_emote in raw_content_info["emote"]:
                emotes.append(each_emote)
            return emotes
        else:
            return None


class Downloader(Progress):
    def __init__(self, oid: int, resource_type: bilibili_api.comment.ResourceType, interval: float):

        super().__init__({"running": "Downloading", "finished": "Downloaded"})
        self.oid = oid
        self.otype = resource_type
        self.interval = interval

        self.pages: List[Page] = []

    async def download_pages(self, page_indexes: Optional[Sequence[int]] = None):
        # 默认下载全部页码评论
        if page_indexes is None:
            page_indexes = list(range(1, (await self.get_page_number()) + 1))

        self.progress_counter.set_progress_total(len(page_indexes))
        pages: List[Page] = []
        for page_index in page_indexes:
            page: Page = await self._download_page(page_index)
            for key in DUPLICATE_KEYS:
                if key in page:
                    del page[key]
            pages.append(page)
            self.progress_counter.inc_progress()
            time.sleep(self.interval)

        self.pages = pages

    async def _download_page(self, page_index=1) -> Page:
        return Page(await bilibili_api.comment.get_comments(oid=self.oid, type_=self.otype, page_index=page_index))

    async def get_page_number(self) -> int:
        raw_data = await bilibili_api.comment.get_comments(oid=self.oid, type_=self.otype, page_index=1)
        return raw_data["page"]["acount"] // raw_data["page"]["size"]