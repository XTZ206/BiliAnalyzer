import logging
from collections import Counter, OrderedDict
from typing import List, Dict, Any

import jieba

from constants import *
from data import Comment, User
from progress import Progress

jieba.setLogLevel(logging.INFO)

Analysis = Dict


class Analyzer(Progress):
    def __init__(self):
        super().__init__(ANALYZER_NAME)
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
            for field in COMMON_FIELDS:
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
                analysis = OrderedDict(
                    sorted(analysis.items(), key=lambda t: t[1], reverse=True))
            return {field: analysis}

        else:
            raise ValueError

    def analyze_basic_info(self, field: Fields) -> Analysis:
        if field not in USER_INFO_FIELDS:
            raise ValueError

        self.counter.set_progress_capacity(len(self.users))
        counter: Dict[Any, int] = {}
        if field == Fields.SEX:
            for user in self.users:
                counter.setdefault(user.sex, 0)
                counter[user.sex] += 1
                self.counter.inc_progress()
        elif field == Fields.LEVEL:
            for user in self.users:
                counter.setdefault(user.level, 0)
                counter[user.level] += 1
                self.counter.inc_progress()
        else:
            for user in self.users:
                counter.setdefault(user.vip, 0)
                counter[user.vip] += 1
                self.counter.inc_progress()
        return counter

    def analyze_verify(self) -> Analysis:
        self.counter.set_progress_capacity(len(self.users))
        counter: Analysis = {}
        for user in self.users:
            verify_type, verify_desc = user.verify
            if verify_type != "无认证":
                counter.setdefault(verify_type, {})
                counter[verify_type][user.name] = verify_desc
            self.counter.inc_progress()
        return counter

    def analyze_sailings(self) -> Analysis:
        self.counter.set_progress_capacity(len(self.users))
        counter: Analysis = {}
        for user in self.users:
            if user.sailings is not None:
                for sailing in user.sailings:
                    counter.setdefault(sailing, 0)
                    counter[sailing] += 1
            self.counter.inc_progress()
        return counter

    def analyze_words(self) -> Analysis:
        self.counter.set_progress_capacity(len(self.comments))
        counter: Analysis = Counter()
        for comment in self.comments:
            if comment.emote is not None:
                message = self.remove_emote(comment.message, comment.emote)
            else:
                message = comment.message
            counter += Counter(jieba.cut(message))
            self.counter.inc_progress()
        return counter

    def analyze_emote(self) -> Analysis:
        self.counter.set_progress_capacity(len(self.comments))
        counter: Analysis = Counter()
        for comment in self.comments:
            if comment.emote is not None:
                counter += Counter(comment.emote)
            self.counter.inc_progress()
        return counter

    @staticmethod
    def remove_emote(message: str, emotion: List) -> str:
        for each_emote in emotion:
            message = message.replace(each_emote, "")
        return message
