from os import PathLike
from typing import Any, TypeAlias
from typing import TypedDict
from collections import Counter

__all__ = [
    "FilePath",
    "Member",
    "Reply",
    "Page",
    "VideoInfo",
    "Cookies",
    "Analysis",
]

FilePath: TypeAlias = str | PathLike[str]


class Member(TypedDict):
    mid: str
    uname: str
    sex: str
    # TODO: type hint the `dict[str, Any]` fields
    level_info: dict[str, Any]
    pendant: dict[str, Any]
    user_sailing: dict[str, Any]
    fans_detail: dict[str, Any]
    vip: dict[str, Any]

    # TODO: unhinted fields
    # sign, avatar, rank, face_nft_new, senior, nameplate, official_verify,
    # user_sailing_v2, is_contractor, contractor_desc, nft_interaction, avatar_item


class Reply(TypedDict):
    rpid: int
    oid: int
    type: int
    mid: int
    root: int
    parent: int
    dialog: int
    member: Member

    # TODO: unhinted fields
    # count, rcount, state, fansgrade, attr, ctime, mid_str, oid_str
    # rpid_str, root_str, parent_str, dialog_str,
    # like, action, content, replies, assist
    # up_action, invisible, card_label, reply_control
    # folder, dynamic_id_str, note_cvid_str, track_info


class Page(TypedDict):
    page: dict[str, int]
    replies: list[Reply] | None
    top: Reply | None

    # TODO: unhinted fields
    # config, upper, vote, blacklist
    # assist, mode, support_mode, control, folder


class VideoInfo(TypedDict):
    pubdate: int
    # TODO: type hint this


class Cookies(TypedDict):
    sessdata: str
    bili_jct: str


class Analysis(TypedDict):
    video_info: VideoInfo
    reply_count: int
    member_count: int
    uid_lengths: Counter[int]
    levels: Counter[int]
    vips: Counter[str]
    sexes: Counter[str]
    pendants: Counter[str]
    cardbags: Counter[str]
    fans_name: str
    fans_count: int
    fans_levels: Counter[int]
    locations: Counter[str]
    comment_intervals: Counter[str]
