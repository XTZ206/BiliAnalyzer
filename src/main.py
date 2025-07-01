import argparse
import json

import auth
from fetch import *
from utils import *


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

    # Analyze Commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze comments from a file")
    analyze_parser.add_argument("input", type=str, help="Input file with comments")
    # TODO: store analysis results in a file

    args = parser.parse_args()

    match args.command:
        case "auth":
            match args.auth_command:
                case "status":
                    print(auth.check())

                case "login":
                    sessdata: str = input("Please enter your sessdata cookie for bilibili: ")
                    bili_jct: str = input("Please enter your bili_jct cookie for bilibili: ")
                    try:
                        credential = auth.login_from_cookies(sessdata=sessdata, bili_jct=bili_jct)
                        with open("credential.json", "w") as f:
                            json.dump({"sessdata": sessdata, "bili_jct": bili_jct}, f, ensure_ascii=False, indent=4)
                        print("BiliAnalyzer Logged In Successfully")
                    except ValueError as error:
                        print(f"Login Failed: {error}")
                        return

                case "logout":
                    auth.logout()
                    print("BiliAnalyzer Logged Out Successfully")

        case "fetch":
            credential = auth.login_from_stored(fake=args.no_auth)
            replies = fetch_replies(args.bvid, limit=args.limit, credential=credential)
            store_replies(replies, filepath=args.output)

        case "analyze":
            replies = load_replies(filepath=args.input)
            members = fetch_members(replies)

            sexes: dict[str, int] = {"男": 0, "女": 0, "保密": 0}
            pendants: dict[str, int] = {}
            locations: dict[str, int] = {}

            for member in members:
                if "sex" in member:
                    sexes[member["sex"]] += 1
                if "pendant" in member and "name" in member["pendant"] and member["pendant"]["name"]:
                    pendants[member["pendant"]["name"]] = pendants.get(member["pendant"]["name"], 0) + 1

            for reply in replies:
                if "reply_control" in reply and "location" in reply["reply_control"]:
                    location = reply["reply_control"]["location"]
                    if location.startswith("IP属地："):
                        location = location[len("IP属地："):]
                    locations[location] = locations.get(location, 0) + 1

            print(f"共分析 {len(replies)} 条评论， {len(members)} 位用户")
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
