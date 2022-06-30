import json
import os.path
import sqlite3
from typing import List, Tuple, NewType, Dict, Literal, Union

from analyzer import Fields, Analysis
from downloader import Comment, User, Page
from progress import Progress

Storage = NewType("Storage", Tuple)


class DatabaseLoader(Progress):
    def __init__(self, fp: str):
        super().__init__({"running": "Loading", "finished": "Loaded"})
        self.fp = fp

    def load(self, table: Literal["Pages", "Comments", "Users"]) -> Union[List[Page], List[Comment], List[User]]:
        storages: List[Storage] = self._get_storages(table)
        if table == "Pages":
            data: List[Page] = []
            self.progress_counter.set_progress_total(len(storages))
            for storage in storages:
                data.append(self.storage_to_page(storage))
                self.progress_counter.inc_progress()
        elif table == "Comments":
            data: List[Comment] = []
            self.progress_counter.set_progress_total(len(storages))
            for storage in storages:
                data.append(self.storage_to_comment(storage))
                self.progress_counter.inc_progress()
        elif table == "Users":
            data: List[User] = []
            self.progress_counter.set_progress_total(len(storages))
            for storage in storages:
                data.append(self.storage_to_user(storage))
                self.progress_counter.inc_progress()
        else:
            raise ValueError
        return data

    def _get_storages(self, table) -> List[Storage]:
        conn = sqlite3.connect(self.fp)
        storages: List[Storage] = conn.execute(f"select * from {table}").fetchall()
        conn.close()
        return storages

    @staticmethod
    def storage_to_page(storage: Storage) -> Page:
        page: Page = json.loads(storage[1])
        return page

    @staticmethod
    def storage_to_comment(storage: Storage) -> Comment:
        comment: Comment = Comment()
        comment.id = storage[0]
        comment.message = storage[1]
        if storage[2] is None:
            comment.emote = None
        else:
            comment.emote = json.loads(storage[2])
        comment.uid = storage[3]
        comment.send_time = storage[4]

        return comment

    @staticmethod
    def storage_to_user(storage: Storage) -> User:
        user = User()
        user.id = storage[0]
        user.name = storage[1]
        user.sex = storage[2]
        user.avatar = storage[3]
        user.level = storage[4]
        user.vip = storage[5]
        if storage[6] == "无认证":
            user.verify = storage[6], None
        else:
            user.verify = storage[6], storage[7]
        if storage[8] is None:
            user.sailings = None
        else:
            user.sailings = json.loads(storage[8])

        return user


class DatabaseDumper(Progress):
    def __init__(self, fp: str):
        super().__init__({"running": "Dumping", "finished": "Dumped"})
        self.fp = fp

        # 检查路径 若路径不存在则创造对应文件夹
        os.makedirs(os.path.dirname(fp), exist_ok=True)

        # 初始化数据库
        conn = sqlite3.connect(self.fp)
        conn.execute("""CREATE TABLE IF NOT EXISTS "Pages"(
                        "INDEX"         INTEGER NOT NULL UNIQUE,
                        "PAGE"          TEXT);""")
        conn.execute("""CREATE TABLE IF NOT EXISTS "Comments"(
                        "RPID"          INTEGER NOT NULL UNIQUE,
                        "MESSAGE"       TEXT,
                        "EMOTION"       TEXT,
                        "UID"           INTEGER NOT NULL,
                        "TIME"          INTEGER NOT NULL);""")
        conn.execute("""CREATE TABLE IF NOT EXISTS "Users"(
                        "UID"           INTEGER NOT NULL UNIQUE,
                        "NAME"          TEXT NOT NULL,
                        "SEX"           TEXT NOT NULL,
                        "AVATAR"        TEXT,
                        "LEVEL"         INTEGER,
                        "VIP"           TEXT,
                        "VERIFY_TYPE"   TEXT,
                        "VERIFY_DESC"   TEXT,
                        "SAILINGS"      TEXT);""")
        conn.execute("""CREATE TABLE IF NOT EXISTS "Analyses"(
                        "FIELD"         TEXT UNIQUE,
                        "ANALYSIS"      TEXT);""")
        conn.commit()
        conn.close()

    def dump(self, table: Literal["Pages", "Comments", "Users", "Analyses"],
             data: Union[List[Comment], List[User], Dict[Fields, Analysis], List[Page]]):
        conn = sqlite3.connect(self.fp)
        if table == "Comments" and isinstance(data, list):
            self.progress_counter.set_progress_total(len(data))
            for comment in data:
                conn.execute("REPLACE INTO Comments "
                             "(\"RPID\", \"MESSAGE\", \"EMOTION\", \"UID\", \"TIME\") "
                             "VALUES (?, ?, ?, ?, ?)",
                             self.comment_to_storage(comment))
                self.progress_counter.inc_progress()

        elif table == "Users" and isinstance(data, list):
            self.progress_counter.set_progress_total(len(data))
            for user in data:
                conn.execute("REPLACE INTO Users "
                             "(\"UID\", \"NAME\", \"SEX\", \"AVATAR\", \"LEVEL\", \"VIP\", "
                             "\"VERIFY_TYPE\", \"VERIFY_DESC\", \"SAILINGS\") "
                             "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             self.user_to_storage(user))
                self.progress_counter.inc_progress()

        elif table == "Analyses" and isinstance(data, dict):
            self.progress_counter.set_progress_total(len(data))
            for field, analysis in data.items():
                conn.execute("REPLACE INTO Analyses "
                             "(\"FIELD\", \"ANALYSIS\") "
                             "VALUES (?, ?)",
                             self.analysis_to_storage(field, analysis))
                self.progress_counter.inc_progress()

        elif table == "Pages" and isinstance(data, list):
            self.progress_counter.set_progress_total(len(data))
            for page in data:
                conn.execute("REPLACE INTO Pages "
                             "(\"INDEX\", \"PAGE\") "
                             "VALUES (?, ?)",
                             self.page_to_storage(page))
                self.progress_counter.inc_progress()

        else:
            raise ValueError

        conn.commit()
        conn.close()

    @staticmethod
    def page_to_storage(page: Page) -> Storage:
        index = page["page"]["num"]
        return Storage((index, json.dumps(page)))

    @staticmethod
    def comment_to_storage(comment: Comment) -> Storage:
        rpid = comment.id
        message = comment.message
        if comment.emote:
            emotion = json.dumps(comment.emote, ensure_ascii=False)
        else:
            emotion = None
        uid = comment.uid
        send_time = comment.send_time

        return Storage((rpid, message, emotion, uid, send_time))

    @staticmethod
    def user_to_storage(user: User) -> Storage:
        uid = user.id
        name = user.name
        sex = user.sex
        avatar = user.avatar
        level = user.level
        vip = user.vip
        verify_type, verify_desc = user.verify
        if user.sailings:
            sailings = json.dumps(user.sailings, ensure_ascii=False)
        else:
            sailings = None

        return Storage((uid, name, sex, avatar, level, vip, verify_type, verify_desc, sailings))

    @staticmethod
    def analysis_to_storage(field: Fields, analysis: Analysis) -> Storage:
        return Storage((field.value, json.dumps(analysis, ensure_ascii=False, indent=4)))
