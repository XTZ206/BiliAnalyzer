import abc
import json
import time
from typing import Collection, Literal, Sequence

import bilibili_api
from PySide6.QtCore import Signal
from bilibili_api import sync, Credential, ResponseCodeException
from bilibili_api.comment import CommentResourceType
from bilibili_api.user import User

from bilianalyzer.storage import CommentStorage, RawData, UserStorage


class Downloader(metaclass=abc.ABCMeta):
    """
    Attributes:
        credential      (Credential)                : 凭据
        storages        (set)                       : 内置数据存储
        progress_signal (Signal | None)             : 进度条信号
        error_logs      (dict[int, Exception])      : 错误记录
    """

    def __init__(self,
                 credential: Credential | None = None,
                 progress_signal: Signal | None = None):
        self.credential: Credential = credential if credential is not None else Credential()
        self.storages: set = set()
        self.progress_signal: Signal | None = progress_signal
        self.error_logs: dict[int, Exception] = {}

    @abc.abstractmethod
    async def get_raw_data(self, index: int) -> RawData | Sequence[RawData]:
        raise NotImplementedError("子类必须实现get_raw_data方法")

    @abc.abstractmethod
    def download(self):
        raise NotImplementedError("子类必须实现download方法")

    def add_storage(self, storage) -> None:
        self.storages.add(storage)

    @abc.abstractmethod
    def get_storages(self, key, reverse: bool) -> list:
        raise NotImplementedError("子类必须实现get_storages方法")

    def has_error_logs(self) -> bool:
        return self.error_logs != {}

    def add_error_logs(self, location: int, error: Exception) -> None:
        self.error_logs[location] = error

    def get_error_logs(self) -> dict:
        return {location: str(error) for location, error in self.error_logs.items()}

    def get_error_logs_serialized(self) -> str:
        return json.dumps(self.get_error_logs(), indent=4, ensure_ascii=False)


class CommentDownloader(Downloader):
    """
    评论下载器

    Attributes:
        oid                 (int)                           : 资源 ID
        otype               (CommentResourceType)           : 资源类枚举
        indexes             (Collection[int])               : 下载索引范围
        credential          (Credential | None, optional)   : 凭据. Defaults to None.
        storages            (set[CommentStorage])           : 评论存储, 无重复
        current_progress    (int)                           : 当前进度
        maximum_progress    (int)                           : 最大进度
        progress_signal     (Signal | None, optional)       : 进度条信号. Defaults to None.
    """

    def __init__(self, oid: int, otype: CommentResourceType,
                 indexes: Collection[int],
                 credential: Credential | None = None,
                 progress_signal: Signal | None = None):
        """
        Args:
            oid             (int)                           : 资源 ID
            otype           (CommentResourceType)           : 资源类枚举
            indexes         (Collection[int])               : 下载范围
            credential      (Credential | None, optional)   : 凭据. Defaults to None.
            progress_signal (Signal | None, optional)       : 更新进度条的信号
        """

        super().__init__(credential, progress_signal)
        self.oid: int = oid
        self.otype: CommentResourceType = otype
        self.indexes: Collection[int] = indexes

        self.storages: set[CommentStorage] = set()

        self.current_progress: int = 0
        self.maximum_progress: int = len(self.indexes)
        self.progress_signal: Signal | None = progress_signal

    async def get_raw_data(self, index: int) -> RawData:
        """
        根据索引获取对应片段评论

        Args:
            index   (int)   : 评论索引

        Returns:
            RawData: API返回结果
        """
        return await bilibili_api.comment.get_comments(oid=self.oid, type_=self.otype,
                                                       page_index=index, credential=self.credential)

    def download(self):
        """
        下载并记录结果
        TODO: 多协程加速下载
        TODO: 代理IP加速
        """
        for progress, index in enumerate(self.indexes):
            try:
                self.current_progress = progress + 1
                coroutine = self.get_raw_data(index)
                raw: dict[str, RawData] = sync(coroutine)

                reply: RawData
                if raw["replies"] is not None:
                    for reply in raw["replies"]:
                        self.add_storage(CommentStorage(raw_data=reply))
            except ResponseCodeException as error:
                self.add_error_logs(index, error)
            finally:
                if self.progress_signal is not None:
                    self.progress_signal.emit(self.current_progress, "下载")
                time.sleep(1)

    def add_storage(self, storage: CommentStorage) -> None:
        """
        添加评论到内置评论存储
        Args:
            storage   (CommentStorage) : 添加的评论
        """
        self.storages.add(storage)

    def get_storages(self,
                     key: Literal["rpid", "user", "time"] | None = None,
                     reverse: bool = False) -> list[CommentStorage]:
        """
        排序后输出评论列表
        Args:
            key     (Literal["rpid", "user", "time"] | None)    : 评论排序方式
            reverse (bool)                                      : 是否倒序
        Return:
            list[CommentStorage]： 评论列表
        """
        if key is not None:
            key_func = {
                "rpid": lambda cmt_st: cmt_st.rpid,
                "user": lambda cmt_st: cmt_st.user.get_uid(),
                "time": lambda cmt_st: cmt_st.time,
            }[key]  # 对应排序方式的处理函数
            return sorted(self.storages, key=key_func, reverse=reverse)
        else:
            return list(self.storages)


class UserDownloader(Downloader):
    """
    Attributes:
        users               (list[User])                    : 需要下载数据的用户
        credential          (Credential | None, optional)   : 凭据. Defaults to None
        storages            (set[UserStorage])              : 用户存储, 无重复
        current_progress    (int)                           : 当前进度
        maximum_progress    (int)                           : 最大进度
        progress_signal     (Signal | None)                 : 更新进度条的信号
    """

    def __init__(self, users: list[User],
                 credential: Credential | None = None,
                 progress_signal: Signal | None = None):
        super().__init__(credential, progress_signal)

        self.users: list[User] = users
        self.credential: Credential | None = credential

        if self.credential is not None:
            for user in self.users:
                user.credential = self.credential

        self.storages: set[UserStorage] = set()

        self.current_progress: int = 0
        self.maximum_progress: int = len(self.users)
        self.progress_signal: Signal | None = progress_signal

    async def get_raw_data(self, index: int) -> Sequence[RawData]:
        user: User = self.users[index]
        return (
            await user.get_user_info(),
            await user.get_all_followings(),
            await user.get_user_medal()
        )

    def download(self):

        for index in range(len(self.users)):
            try:
                self.current_progress = index + 1
                coroutine = self.get_raw_data(index)
                self.add_storage(UserStorage(raw_data=sync(coroutine)))
            except ResponseCodeException as error:
                self.add_storage(UserStorage())
                self.add_error_logs(index, error)
            finally:
                if self.progress_signal is not None:
                    self.progress_signal.emit(self.current_progress, "分析")
                time.sleep(1)

    def add_storage(self, storage: UserStorage) -> None:
        """
        添加用户到内置用户存储
        Args:
            storage    (UserStorage)    : 添加的用户
        """
        self.storages.add(storage)

    def get_storages(self,
                     key: Literal["uid", "name", "level"] | None = None,
                     reverse: bool = False):
        if key is not None:
            key_func = {
                "uid": lambda usr_st: usr_st.uid,
                "name": lambda usr_st: usr_st.name,
                "level": lambda usr_st: usr_st.level,
            }[key]  # 对应排序方式的处理函数
            return sorted(self.storages, key=key_func, reverse=reverse)
        else:
            return list(self.storages)


if __name__ == '__main__':
    with open("credential", "r", encoding="utf-8") as f:
        cdt = Credential(**(json.load(f)))
        ud = UserDownloader([User(20165629)], cdt)
        res = sync(ud.get_raw_data(0))
