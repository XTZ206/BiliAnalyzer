import argparse
import asyncio
import json

from bilibili_api import Credential

from . import auth
from .fetch.comments import Fetcher, save_replies, load_replies, save_video_info, load_video_info
from .analyze.comments import CommentAnalyzer, save_analysis
from .utils import *


async def main() -> None:
    parser = argparse.ArgumentParser(prog="bilianalyzer", usage="%(prog)s [command]", description="Fetch and Analyze Bilibili Comments")
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
    fetch_parser.add_argument("-n", "--limit", type=int, default=10, help="Limit the maximum number of pages to fetch (default: 10)")
    fetch_parser.add_argument("-o", "--output", type=str, default="comments.json", help="Output filepath for comments (default: comments.json)")
    fetch_parser.add_argument("--no-auth", action="store_true", help="Skip authentication and fetch comments without credentials")

    # Analyze Commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze comments from a file")
    analyze_parser.add_argument("input", type=str, help="Input file with comments")
    analyze_parser.add_argument("-o", "--output", type=str, default="analysis_results.json", help="Output filepath for analysis results (default: analysis_results.json)")

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
            fetcher = Fetcher(credential)
            replies = await fetcher.fetch_replies(args.bvid, limit=args.limit)
            video_info = await fetcher.fetch_video_info(args.bvid)
            save_replies(replies, filepath=args.output)

            # TODO: replace hardcoded video_info filepath
            save_video_info(video_info, filepath="video_info.json")

        case "analyze":
            # TODO: replace hardcoded video_info filepath
            video_info = load_video_info(filepath="video_info.json")
            replies = load_replies(filepath=args.input)
            analyzer = CommentAnalyzer(video_info, replies)
            analysis: Analysis = analyzer.generate_analysis()

            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(analysis, f, ensure_ascii=False, indent=4)

            # 命令行格式化输出分析报告
            print("=" * 40)
            print("BiliAnalyzer 评论分析报告")
            print("=" * 40)
            print(f"评论数量: {analysis.get('评论数量', analysis.get('reply_count', 0))}")
            print(f"用户数量: {analysis.get('用户数量', analysis.get('member_count', 0))}")
            print()

            def print_dist(title, dist, unit="个", top=5):
                print(f"{title}:")
                if isinstance(dist, dict):
                    items = list(dist.items())
                elif hasattr(dist, "most_common"):
                    items = dist.most_common(top)
                else:
                    items = []
                if len(items) == 0:
                    print("无数据")
                else:
                    for k, v in items[:top]:
                        print(f"  {k}: {v} {unit}")
                    if len(items) > top:
                        print("  ...")
                print()

            # 基础信息
            print(f"共分析 {analysis['reply_count']} 条评论，来自 {analysis['member_count']} 位用户")

            # 用户分布信息

            print_dist("用户UID位数分布", analysis["uid_lengths"], "次")
            print_dist("用户等级分布", analysis["levels"], "个")
            print_dist("用户大会员分布", analysis["vips"], "个")
            print_dist("用户性别分布", analysis["sexes"], "个")
            print_dist("用户头像框分布", analysis["pendants"], "次")
            print_dist("用户数字周边分布", analysis["cardbags"], "次")

            print(f"粉丝团名称: {analysis['fans_name']}")
            print(f"粉丝团成员总数: {analysis['fans_count']}")
            print_dist("粉丝团等级分布", analysis["fans_levels"], "个")
            print_dist("评论IP属地分布", analysis["locations"], "次")
            print_dist("评论发布时间分布", analysis["comment_intervals"], "次")

            print("=" * 40)
            print(f"分析结果已保存到 {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
