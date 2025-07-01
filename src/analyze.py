from collections import Counter
from utils import *


def analyze_sexes(members: Collection[Member]) -> Counter[str]:
    return Counter(member.get("sex", "保密") for member in members)


def analyze_pendants(members: Collection[Member]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for member in members:
        if "pendant" not in member:
            continue
        if "name" not in member["pendant"]:
            continue
        pendant: str = member.get("pendant", {}).get("name", "").strip()
        if pendant:
            counter.update(pendant)
    return counter


def analyze_locations(replies: Collection[Reply]) -> Counter[str]:
    prefix: str = "IP属地："
    counter: Counter[str] = Counter()
    for reply in replies:
        if "reply_control" not in reply:
            continue
        if "location" not in reply["reply_control"]:
            continue
        location: str = reply["reply_control"]["location"]
        if location.startswith(prefix):
            counter.update(location[len(prefix):])
    return counter
