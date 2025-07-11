import json
import os
from collections import Counter, defaultdict
from utils import *
from datetime import datetime

TIME_INTERVALS = {
    "半小时内": (0, 0.5),
    "0.5-1小时内": (0.5, 1),
    "1-2小时内": (1, 2),
    "2-3小时内": (2, 3),
    "3-6小时内": (3, 6),
    "6-12小时内": (6, 12),
    "12-24小时内（1天内）": (12, 24),
    "24-48小时内（2天内）": (24, 48),
    "48-72小时内（3天内）": (48, 72),
    "3天以上": (72, float("inf"))
}


def analyze_uid_lengths(members: Collection[Member]) -> Counter[int]:
    return Counter(len(member["mid"]) for member in members)


def analyze_levels(members: Collection[Member]) -> Counter[int]:
    return Counter(member["level_info"]["current_level"] + member["is_senior_member"]
                   for member in members)


def analyze_vips(members: Collection[Member]):
    # TODO: analyze the vip remaining days
    vips: Counter[str] = Counter()

    for member in members:
        if member["vip"]["vipStatus"] == 0:
            vips["非大会员"] += 1
        else:
            vips[member["vip"]["label"]["text"]] += 1

    return vips


def analyze_sexes(members: Collection[Member]) -> Counter[str]:
    return Counter(member.get("sex", "保密") for member in members)


def analyze_pendants(members: Collection[Member]) -> Counter[str]:
    # NOTE: pendant 表示头像框，叠加在头像上
    pendants: Counter[str] = Counter()
    for member in members:
        if member.get("pendant") is None:
            continue
        pendant: str = member["pendant"].get("name", "").strip()
        if pendant:
            pendants[pendant] += 1
    return pendants


def analyze_cardbgs(members: Collection[Member]) -> Counter[str]:
    # NOTE: cardbg 表示数字周边，出现在评论右侧
    cardbgs: Counter[str] = Counter()
    for member in members:
        if member.get("user_sailing") is None:
            continue
        if member["user_sailing"].get("cardbg") is None:
            continue

        cardbg: str = member["user_sailing"]["cardbg"].get("name", "").strip()
        if cardbg:
            cardbgs[cardbg] += 1
    return cardbgs


def analyze_fans(members: Collection[Member]) -> tuple[str, Counter[int]]:
    fans_name: str = "未知粉丝团"
    fans_levels: Counter[int] = Counter()
    for member in members:
        if member.get("fans_detail") is None:
            continue

        if fans_name == "未知粉丝团":
            fans_name = member["fans_detail"].get("medal_name", "未知粉丝团").strip()

        fans_level: int = member["fans_detail"].get("level", 0)
        fans_levels[fans_level] += 1
    return fans_name, fans_levels


def analyze_locations(replies: Collection[Reply]) -> Counter[str]:
    prefix: str = "IP属地："
    locations: Counter[str] = Counter()
    for reply in replies:
        if "reply_control" not in reply:
            continue
        if "location" not in reply["reply_control"]:
            continue
        location: str = reply["reply_control"]["location"]
        if location.startswith(prefix):
            locations[location[len(prefix):]] += 1
    return locations


def save_results(results: Analysis, filepath: FilePath) -> None:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def analyze_comment_times(video_info: list[VideoInfo], replies: Collection[Reply]) -> Counter[str]:
    video_pubdate: int = video_info[0]["pubdate"]
    interval_dict: dict[str, int] = defaultdict(int)
    for reply in replies:
        ctime = reply.get("ctime")
        if not ctime:
            continue
        time_interval: int = ctime - video_pubdate
        if time_interval < 0:
            continue
        for interval_name, (start, end) in TIME_INTERVALS.items():
            if start * 3600 <= time_interval < end * 3600:
                interval_dict[interval_name] += 1
                break
    return Counter(interval_dict)
