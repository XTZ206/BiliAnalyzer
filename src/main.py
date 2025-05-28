import asyncio
import argparse
import json
from typing import Optional

from bilibili_api import sync, bvid2aid, Credential
from bilibili_api.video import Video
from bilibili_api.comment import get_comments, CommentResourceType


async def get_replies(bvid: str, limit: int = 10, credential: Optional[Credential] = None) -> list[dict]:
    replies = []
    page = 1
    count = 0
    while True:
        if page > 1:
            await asyncio.sleep(1)
        comments = await get_comments(bvid2aid(bvid), CommentResourceType.VIDEO, page, credential=credential)
        if not comments or "replies" not in comments or "page" not in comments:
            break
        if not comments["replies"] or not comments["page"]:
            break
        replies.extend(comments["replies"])
        count += comments["page"]["size"]
        page += 1
        if page > limit or count > comments["page"]["count"]:
            break

    return replies


def get_users(replies: list[dict]) -> list[dict]:
    users: list[dict] = []
    names: set[str] = set()
    for reply in replies:
        user = reply.get("member", {})
        name = user.get("uname", None)
        if name is None or name in names:
            continue
        names.add(name)
        users.append(user)
    return users


def main() -> None:
    parser = argparse.ArgumentParser(prog="bilianalyzer", usage="%(prog)s [command]",
                                     description="Fetch and Analyze Bilibili Comments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Authentication commands
    auth_parser = subparsers.add_parser("auth", help="Authenticate BiliAnalyzer with Bilibili Cookies")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)
    auth_subparsers.add_parser("status", help="Check Authentication Status of BiliAnalyzer")
    auth_subparsers.add_parser("login", help="Login and Store Cookies for BiliAnalyzer")
    auth_subparsers.add_parser("logout", help="Logout BiliAnalyzer and Remove Stored Cookies")

    # Fetch Commands
    fetch_parser = subparsers.add_parser("fetch", help="Fetch comments for a video with given BVID")
    fetch_parser.add_argument("bvid", type=str, help="BVID of the video")
    fetch_parser.add_argument("-n", "--limit", type=int, default=10,
                              help="Limit the maximum number of pages to fetch (default: 10)")
    fetch_parser.add_argument("-o", "--output", type=str, default="comments.json",
                              help="Output filepath for comments (default: comments.json)")
    fetch_parser.add_argument("--no-auth", action="store_true",
                              help="Skip authentication and fetch comments without credentials")
    # TODO: fetch sub replies

    # Analyze Commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze comments from a file")
    analyze_parser.add_argument("input", type=str, help="Input file with comments")
    # TODO: store analysis results in a file

    args = parser.parse_args()

    match args.command:
        case "auth":
            match args.auth_command:
                case "status":
                    credential: Optional[Credential] = None
                    with open("credential.json", "r") as f:
                        credential = Credential(**json.load(f))
                    if credential is None or credential.sessdata is None or credential.bili_jct is None:
                        print("BiliAnalyzer Not Authenticated")
                    elif not sync(credential.check_valid()):
                        print("BiliAnalyzer Authentication Expired")
                    else:
                        print("BiliAnalyzer Authenticated Successfully")

                case "login":
                    sessdata: str = input("Please enter your sessdata cookie for bilibili: ")
                    bili_jct: str = input("Please enter your bili_jct cookie for bilibili: ")
                    credential = Credential(sessdata=sessdata, bili_jct=bili_jct)
                    with open("credential.json", "w") as f:
                        json.dump({"sessdata": sessdata, "bili_jct": bili_jct}, f, ensure_ascii=False, indent=4)
                    if sync(credential.check_valid()):
                        print("BiliAnalyzer Authenticated Successfully")
                    else:
                        print("BiliAnalyzer Authentication Failed. Please check your cookies.")

                case "logout":
                    with open("credential.json", "w") as f:
                        json.dump({"sessdata": None, "bili_jct": None}, f, ensure_ascii=False, indent=4)
                    print("BiliAnalyzer Logged Out Successfully")

        case "fetch":
            if args.no_auth:
                credential = None
            else:
                with open("credential.json", "r") as f:
                    credential = Credential(**json.load(f))
            replies = sync(get_replies(args.bvid, limit=args.limit, credential=credential))

            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(replies, f, ensure_ascii=False, indent=4)

        case "analyze":
            with open(args.input, "r", encoding="utf-8") as f:
                replies = json.load(f)
            users = get_users(replies)
            sexes: dict[str, int] = {"男": 0, "女": 0, "保密": 0}
            pendants: dict[str, int] = {}
            locations: dict[str, int] = {}

            for user in users:
                if "sex" in user:
                    sexes[user["sex"]] += 1
                if "pendant" in user and "name" in user["pendant"] and user["pendant"]["name"]:
                    pendants[user["pendant"]["name"]] = pendants.get(user["pendant"]["name"], 0) + 1

            for reply in replies:
                if "reply_control" in reply and "location" in reply["reply_control"]:
                    location = reply["reply_control"]["location"]
                    if location.startswith("IP属地："):
                        location = location[len("IP属地："):]
                    locations[location] = locations.get(location, 0) + 1

            print(f"共分析 {len(replies)} 条评论， {len(users)} 位用户")
            print("用户性别分布：")
            print(f"男: {sexes['男']}\n女: {sexes['女']}\n保密: {sexes['保密']}")
            print()

            if len(pendants) == 0:
                print("没有用户展示了装扮")
            else:
                print("用户装扮分布：")
                top_n = 5  # 可根据需要修改n的值
                for pendant, count in sorted(pendants.items(), key=lambda x: x[1], reverse=True)[:top_n]:
                    print(f"{pendant}: {count} 次")
                if (len(pendants) > top_n):
                    print(f"... 其他{len(pendants) - top_n}个装扮")
            print()

            print("评论IP属地分布：")
            top_n = 5  # 可根据需要修改n的值
            for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:top_n]:
                print(f"{location}: {count} 次")
            if (len(locations) > top_n):
                print(f"... 其他{len(locations) - top_n}个IP属地")


if __name__ == "__main__":
    main()
