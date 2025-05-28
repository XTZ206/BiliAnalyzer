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


def main() -> None:
    parser = argparse.ArgumentParser(prog="bilianalyzer", usage="%(prog)s [command]",
                                     description="Fetch and Analyze Bilibili Comments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_parser = subparsers.add_parser("auth", help="Authenticate BiliAnalyzer with Bilibili Cookies")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)
    auth_subparsers.add_parser("status", help="Check Authentication Status of BiliAnalyzer")
    auth_subparsers.add_parser("login", help="Login and Store Cookies for BiliAnalyzer")
    auth_subparsers.add_parser("logout", help="Logout BiliAnalyzer and Remove Stored Cookies")

    fetch_parser = subparsers.add_parser("fetch",
                                         help="Fetch comments for a video with given BVID")
    fetch_parser.add_argument("bvid", type=str,
                              help="BVID of the video")

    analyze_parser = subparsers.add_parser("analyze",
                                           help="Analyze comments from a file")
    analyze_parser.add_argument("input", type=str,
                                help="Input file with comments")

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
            with open("credential.json", "r") as f:
                credential = Credential(**json.load(f))
            replies = sync(get_replies(args.bvid, credential=credential))
            with open(f"comments_{args.bvid}.json", "w", encoding="utf-8") as f:
                json.dump(replies, f, ensure_ascii=False, indent=4)

        case "analyze":
            with open(args.input, "r", encoding="utf-8") as f:
                replies = json.load(f)
            users: dict[str, dict] = {}
            sexes: dict[str, int] = {"男": 0, "女": 0, "保密": 0}
            pendants: dict[str, int] = {}

            for reply in replies:
                member = reply.get("member", {})
                name = member.get("uname", "未知")
                users[name] = member

            for name, user in users.items():
                sexes[user.get("sex", "保密")] += 1
                pendant_name = user.get("pendant", {}).get("name", "")
                if pendant_name:
                    pendants[pendant_name] = pendants.get(pendant_name, 0) + 1

            print(f"共分析 {len(replies)} 条评论， {len(users)} 位用户")
            print("用户性别分布：")
            print(f"男: {sexes['男']}, 女: {sexes['女']}, 保密: {sexes['保密']}")

            if len(pendants) == 0:
                print("没有用户装扮数据")
            else:
                print("用户装扮分布：")

                top_n = 5  # 可根据需要修改n的值
                for pendant, count in sorted(pendants.items(), key=lambda x: x[1], reverse=True)[:top_n]:
                    print(f"{pendant}: {count} 次")
                if (len(pendants) > top_n):
                    print(f"... 其他{len(pendants) - top_n}个装扮")


if __name__ == "__main__":
    main()
