import logging
from collections import Counter, OrderedDict
from enum import Enum
from typing import List, Dict

import jieba

from data import Comment, User
from progress import Progress

jieba.setLogLevel(logging.INFO)


class Fields(Enum):
    ALL = "all"
    WHOLE = "all"
    WORDS = "words"
    EMOTE = "emote"
    SEX = "sex"
    GENDER = "sex"
    LEVEL = "level"
    VIP = "vip"
    VERIFY = "verify"
    SAILINGS = "sailings"


SPECIAL_FIELDS = (Fields.ALL, Fields.WHOLE)
COMMENT_FIELDS = (Fields.WORDS, Fields.EMOTE)
USER_FIELDS = (Fields.SEX, Fields.LEVEL, Fields.VIP, Fields.VERIFY, Fields.SAILINGS)
USER_INFO_FIELDS = (Fields.SEX, Fields.LEVEL, Fields.VIP)
SINGLE_FIELDS = COMMENT_FIELDS + USER_FIELDS
SORTABLE_FIELDS = (Fields.WORDS, Fields.EMOTE, Fields.SEX, Fields.LEVEL, Fields.VIP, Fields.SAILINGS)

Analysis = Dict


class Analyzer(Progress):
    def __init__(self):
        super().__init__({"running": "Analyzing", "finished": "Analyzed"})
        self.comments: List[Comment] = []
        self.users: List[User] = []
        self.has_data = False

    def set_data(self, comments: List[Comment], users: List[User]):
        self.comments: List[Comment] = comments
        self.users: List[User] = users
        self.has_data = True

    def analyze(self, field: Fields) -> Dict[Fields, Analysis]:
        assert self.has_data

        if field in SPECIAL_FIELDS:
            analyses = {}
            for field in SINGLE_FIELDS:
                analyses[field] = self.analyze(field)[field]
            return analyses
        elif field in COMMENT_FIELDS or field in USER_FIELDS:
            if field in USER_INFO_FIELDS:
                analysis = self.analyze_basic_info(field)
            elif field in USER_FIELDS:
                if field == Fields.VERIFY:
                    analysis = self.analyze_verify()
                else:
                    analysis = self.analyze_sailings()
            else:
                if field == Fields.WORDS:
                    analysis = self.analyze_words()
                else:
                    analysis = self.analyze_emote()
            if field in SORTABLE_FIELDS:
                analysis = OrderedDict(sorted(analysis.items(), key=lambda t: t[1], reverse=True))
            return {field: analysis}

        else:
            raise ValueError

    def analyze_basic_info(self, field: Fields) -> Analysis:
        if field not in USER_INFO_FIELDS:
            raise ValueError

        self.progress_counter.set_progress_total(len(self.users))
        counter = {}
        if field == Fields.SEX:
            for user in self.users:
                counter.setdefault(user.sex, 0)
                counter[user.sex] += 1
                self.progress_counter.inc_progress()
        elif field == Fields.LEVEL:
            for user in self.users:
                counter.setdefault(user.level, 0)
                counter[user.level] += 1
                self.progress_counter.inc_progress()
        else:
            for user in self.users:
                counter.setdefault(user.vip, 0)
                counter[user.vip] += 1
                self.progress_counter.inc_progress()
        return counter

    def analyze_verify(self) -> Analysis:
        self.progress_counter.set_progress_total(len(self.users))
        counter: Analysis = {}
        for user in self.users:
            verify_type, verify_desc = user.verify
            if verify_type != "无认证":
                counter.setdefault(verify_type, {})
                counter[verify_type][user.name] = verify_desc
            self.progress_counter.inc_progress()
        return counter

    def analyze_sailings(self) -> Analysis:
        self.progress_counter.set_progress_total(len(self.users))
        counter: Analysis = {}
        for user in self.users:
            if user.sailings is not None:
                for sailing in user.sailings:
                    counter.setdefault(sailing, 0)
                    counter[sailing] += 1
            self.progress_counter.inc_progress()
        return counter

    def analyze_words(self) -> Analysis:
        self.progress_counter.set_progress_total(len(self.comments))
        counter: Analysis = Counter()
        for comment in self.comments:
            if comment.emote is not None:
                message = self.remove_emote(comment.message, comment.emote)
            else:
                message = comment.message
            counter += Counter(jieba.cut(message))
            self.progress_counter.inc_progress()
        return counter

    def analyze_emote(self) -> Analysis:
        self.progress_counter.set_progress_total(len(self.comments))
        counter: Analysis = Counter()
        for comment in self.comments:
            if comment.emote is not None:
                counter += Counter(comment.emote)
            self.progress_counter.inc_progress()
        return counter

    @staticmethod
    def remove_emote(message: str, emotion: List) -> str:
        for each_emote in emotion:
            message = message.replace(each_emote, "")
        return message
