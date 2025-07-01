import json
import os
from typing import Any, Dict, List, Optional
from collections import Counter
import time

# Type definitions
Page = Dict[str, Any]
Reply = Dict[str, Any]

def extract_mid_from_reply(reply: Reply) -> Optional[int]:
    #Extract user mid from comment reply
    member = reply.get("member", {})
    return member.get("mid")

def extract_location_from_reply(reply: Reply) -> Optional[str]:
    #Extract IP location from comment reply
    content = reply.get("content", {})
    return content.get("location")

def store_replies(replies: List[Reply], filepath: str) -> None:
    #Save comments to JSON file
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False, indent=4)

def load_replies(filepath: str) -> List[Reply]:
    #Load comments from JSON file
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_members(replies: List[Reply]) -> List[Dict]:
    #Extract all user information from comment list
    return [r.get("member", {}) for r in replies]

def analyze_sexes(members: List[Dict]) -> Counter[str]:
    #Analyze user gender distribution
    sexes = [m.get("sex", "保密") for m in members]  # "保密" remains as is (meaning "Private" in Chinese)
    return Counter(sexes)

def analyze_pendants(members: List[Dict]) -> Counter[str]:
    #Analyze user pendant distribution
    pendants = [m.get("pendant", {}).get("name", "无装扮") for m in members]  # "无装扮" remains as is (meaning "No pendant")
    return Counter(pendants)

def analyze_locations(replies: List[Reply]) -> Counter[str]:
    #Analyze comment IP location distribution
    locations = [extract_location_from_reply(r) for r in replies]
    return Counter(l for l in locations if l)

def filter_comments(
    comments: List[Reply],
    min_likes: int = 0,
    start_date: str = None,
    end_date: str = None
) -> List[Reply]:
    #Filter comment list
    filtered = []
    for comment in comments:
        # Filter by number of likes
        if comment.get("like", 0) < min_likes:
            continue
        
        # Filter by date
        if start_date or end_date:
            ctime = comment.get("ctime", 0)
            date_str = time.strftime("%Y-%m-%d", time.localtime(ctime))
            if start_date and date_str < start_date:
                continue
            if end_date and date_str > end_date:
                continue
                
        filtered.append(comment)
    return filtered