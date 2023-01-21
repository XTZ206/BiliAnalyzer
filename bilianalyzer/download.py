import time
from typing import Collection, NewType, Literal

import bilibili_api
from PySide6.QtCore import Signal
from bilibili_api import sync, Credential
from bilibili_api.comment import CommentResourceType

from exceptions import CheckingException
from storage import CommentStorage, RawData




class CommentDownloader:
    """
    评论下载器

    Attributes:
        oid                 (int)                           : 资源 ID
        otype               (CommentResourceType)           : 资源类枚举
        indexes             (Collection[int])               : 下载索引范围
        is_checked          (bool)                          : 是否已检查参数
        credential          (Credential | None, optional)   : 凭据. Defaults to None.
        comment_storages    (set[CommentStorage])           : 评论存储, 使用set去重
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

        self.oid: int = oid
        self.otype: CommentResourceType = otype
        self.indexes: Collection[int] = indexes
        self.is_checked: bool = False
        self.credential: Credential | None = credential
        self.comment_storages: set[CommentStorage] = set()

        self.current_progress: int = 0
        self.maximum_progress: int = len(self.indexes)
        self.progress_signal: Signal | None = progress_signal

    def check_arguments(self):
        """
        检查传入的资源ID和索引范围是否有效
        """
        try:
            self.oid = int(self.oid)
        except ValueError:
            raise ValueError("资源ID必须为数字")
        if len(self.indexes) == 0:
            raise ValueError("索引范围不能为空")
        for index in self.indexes:
            if index <= 0:
                raise ValueError("索引必须都为正整数")

        self.is_checked = True

    async def get_raw_data(self, index=1) -> RawData:
        """
        根据索引获取对应片段评论

        Args:
            index   (int)   : 评论索引

        Returns:
            RawData: API返回结果
        """
        return RawData(await bilibili_api.comment.get_comments(oid=self.oid, type_=self.otype, page_index=index,
                                                               credential=self.credential))

    # TODO: 多协程同时下载
    def download(self):
        """
        下载并记录结果
        """
        if not self.is_checked:
            raise CheckingException("下载前未检查传入参数")

        for progress, index in enumerate(self.indexes):
            self.current_progress = progress + 1
            coroutine = self.get_raw_data(index)
            raw: dict[str, RawData] = sync(coroutine)

            reply: RawData
            if raw["replies"] is not None:
                for reply in raw["replies"]:
                    if CommentStorage(reply) not in self.comment_storages:
                        self.add_comment(CommentStorage(reply))
                if self.progress_signal is not None:
                    self.progress_signal.emit(self.current_progress)
            time.sleep(1)

    def add_comment(self, comment_storage: "CommentStorage") -> None:
        """
        添加评论到内置评论存储
        Args:
            comment_storage   (CommentStorage) : 添加的评论
        """
        if comment_storage not in self.comment_storages:
            self.comment_storages.add(comment_storage)

    def output_comments(self,
                        key: Literal["rpid", "user", "time"] | None = None,
                        reverse: bool = False) -> list["CommentStorage"]:
        """
        排序后
        Args:
            key     (Literal["rpid", "user", "time"] | None)    : 评论排序方式
            reverse (bool)                                      : 是否倒序
        Return:
            list[comment_storage]： 评论列表
        """
        if key is not None:
            key_func = {
                "rpid": lambda cmt_st: cmt_st.rpid,
                "user": lambda cmt_st: cmt_st.user.get_uid(),
                "time": lambda cmt_st: cmt_st.time,
            }[key]  # 对应排序方式的处理函数
            return sorted(self.comment_storages, key=key_func, reverse=reverse)
        else:
            return list(self.comment_storages)
