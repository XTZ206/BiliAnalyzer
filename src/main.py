import argparse
import json

import auth
from fetch import *
from analyze import *
from utils import *


async def main() -> None:
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
    analyze_parser.add_argument("-o", "--output", type=str, default="analysis_results.json",
                                help="Output filepath for analysis results (default: analysis_results.json)")

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
                    except ValueError as error:
                        print(f"Login Failed: {error}")
                        return
                    print("BiliAnalyzer Logged In Successfully")

                case "logout":
                    auth.logout()
                    print("BiliAnalyzer Logged Out Successfully")

        case "fetch":
            credential: Credential = Credential()
            if not args.no_auth:
                try:
                    credential = auth.load_credential()
                except ValueError as error:
                    print(f"Authentication Failed: {error}")
                    return
            replies = await fetch_replies(args.bvid, limit=args.limit, credential=credential)
            video_info= await fetch_video_info(args.bvid, credential=credential)
            save_replies(replies, filepath=args.output)
            save_video_info(video_info, filepath="video_info.json")

        case "analyze":
            replies = load_replies(filepath=args.input)
            members = fetch_members(replies)

            uid_lengths: Counter[int] = analyze_uid_lengths(members)
            levels: Counter[int] = analyze_levels(members)
            vips: Counter[str] = analyze_vips(members)
            sexes: Counter[str] = analyze_sexes(members)
            pendants: Counter[str] = analyze_pendants(members)
            cardbgs: Counter[str] = analyze_cardbgs(members)
            fan_name, fan_levels = analyze_fans(members)
            locations: Counter[str] = analyze_locations(replies)
            comment_time_distribution: Counter[str,int] = analyze_comment_times(load_video_info("video_info.json"),replies)

            print(f"共分析 {len(replies)} 条评论， {len(members)} 位用户")

            print("用户UID位数分布: ")
            for uid_length, count in uid_lengths.most_common():
                print(f"{uid_length} 位: {count} 次")
            print()

            print("用户等级分布:")
            for level, count in levels.most_common():
                if level == 7:
                    print(f"硬核: {count:<3}个")
                else:
                    print(f"{level} 级: {count:<3}个")
            print()

            print("用户大会员分布:")
            for vip, count in vips.most_common():
                print(f"{vip}: {count} 个")
            print()

            print("用户性别分布:")
            print(f"男: {sexes['男']}个")
            print(f"女: {sexes['女']}个")
            print(f"保密: {sexes['保密']}个")
            print()

            print("用户头像框分布:")
            print(f"共计{len(pendants)}种头像框")
            if len(pendants) == 0:
                print("没有用户展示了头像框")
            else:
                for pendant, count in pendants.most_common(5):
                    print(f"{pendant}: {count} 次")
                if len(pendants) > 5:
                    print("...")
            print()

            print("用户数字周边分布:")
            print(f"共计{len(cardbgs)}种数字周边")
            if len(cardbgs) == 0:
                print("没有用户展示了数字周边")
            else:
                for cardbg, count in cardbgs.most_common(5):
                    print(f"{cardbg}: {count} 次")
                if len(cardbgs) > 5:
                    print("...")
            print()

            print(f"粉丝团 {fan_name} 等级分布:")
            print(f"共计 {sum(fan_levels.values())} 个粉丝团成员")
            for level, count in fan_levels.most_common():
                print(f"{level} 级: {count} 个")
            print()

            print("评论IP属地分布:")
            print(f"共计{len(locations)}种属地分布")
            for location, count in locations.most_common(5):
                print(f"{location}: {count} 次")
            if len(locations) > 5:
                print("...")
            print()
            print("评论发布时间分布:")
            for time, count in comment_time_distribution.most_common():
                print(f"{time}: {count} 次")        
            print()

            analysis: Analysis = {
                "评论数量": len(replies),
                "用户数量": len(members),
                "用户UID位数分布": {f"{k}位": v for k, v in uid_lengths.items()},
                "用户等级分布": {f"{k}级" if k != 7 else "硬核": v for k, v in levels.items()},
                "用户大会员分布": dict(vips),
                "用户性别分布": dict(sexes),
                "用户头像框分布": dict(pendants),
                "用户数字周边分布": dict(cardbgs),
                "粉丝团信息": {
                    "粉丝团名称": fan_name,
                    "粉丝团等级分布": dict(fan_levels),
                    "粉丝团成员总数": sum(fan_levels.values())
                },
                "评论IP属地分布": dict(locations),
                "评论发布时间分布": dict(comment_time_distribution)
            }
            save_results(analysis, args.output)
            print(f"分析结果已保存到 {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
