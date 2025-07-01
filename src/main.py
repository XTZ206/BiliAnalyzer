import argparse
import json

import auth
from fetch import fetch_replies
from analyze import analyze_comments
from utils import store_replies, load_replies
from config import load_config, save_config, get_config_value

def main() -> None:
    # Load configuration
    config = load_config()
    
    parser = argparse.ArgumentParser(
        prog="bilianalyzer",
        usage="%(prog)s [command]",
        description="Fetch and Analyze Bilibili Comments"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Authentication commands
    auth_parser = subparsers.add_parser("auth", help="Authenticate BiliAnalyzer with Bilibili Cookies")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)
    auth_subparsers.add_parser("status", help="Check Authentication Status of BiliAnalyzer")
    auth_subparsers.add_parser("login", help="Login and Store Cookies for BiliAnalyzer")
    auth_subparsers.add_parser("logout", help="Logout BiliAnalyzer and Remove Stored Cookies")

    # Configuration commands
    config_parser = subparsers.add_parser("config", help="Manage BiliAnalyzer settings")
    config_subparsers = config_parser.add_subparsers(dest="config_command", required=True)
    
    # Set configuration item
    set_parser = config_subparsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("key", type=str, help="Config key (e.g., output_dir, page_size, sort_order)")
    set_parser.add_argument("value", type=str, help="Config value")
    
    # View configuration
    show_parser = config_subparsers.add_parser("show", help="Show current configuration")
    show_parser.add_argument("--key", type=str, help="Specific config key to show")

    # Fetch comments command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch comments for a video with given BVID")
    fetch_parser.add_argument("bvid", type=str, help="BVID of the video")
    fetch_parser.add_argument("-n", "--limit", type=int, default=config.get("page_size", 20),
                              help=f"Limit the maximum number of pages to fetch (default: {config.get('page_size', 20)})")
    fetch_parser.add_argument("-o", "--output", type=str, default=config.get("output_dir", "output/") + "comments.json",
                              help=f"Output filepath for comments (default: {config.get('output_dir', 'output/')}comments.json)")
    fetch_parser.add_argument("--no-auth", action="store_true",
                              help="Skip authentication and fetch comments without credentials")
    fetch_parser.add_argument("--sort", type=str, default=config.get("sort_order", "time"), choices=["time", "like"],
                              help=f"Sort comments by time or like (default: {config.get('sort_order', 'time')})")
    fetch_parser.add_argument("--min-likes", type=int, default=0,
                              help="Minimum likes required for comments")
    fetch_parser.add_argument("--start-date", type=str,
                              help="Start date (YYYY-MM-DD) to filter comments")
    fetch_parser.add_argument("--end-date", type=str,
                              help="End date (YYYY-MM-DD) to filter comments")

    # Analyze comments command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze comments from a file")
    analyze_parser.add_argument("input", type=str, help="Input file with comments")
    analyze_parser.add_argument("-o", "--output", type=str, default=config.get("output_dir", "output/") + "analysis/",
                              help=f"Output directory for analysis results (default: {config.get('output_dir', 'output/')}analysis/)")
    analyze_parser.add_argument("--start-date", type=str,
                              help="Start date (YYYY-MM-DD) to analyze comments")
    analyze_parser.add_argument("--end-date", type=str,
                              help="End date (YYYY-MM-DD) to analyze comments")

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

        case "config":
            match args.config_command:
                case "set":
                    config[args.key] = args.value
                    save_config(config)
                    print(f"Config '{args.key}' set to '{args.value}'")
                
                case "show":
                    if args.key:
                        print(f"{args.key}: {config.get(args.key, 'Not set')}")
                    else:
                        print(json.dumps(config, indent=2, ensure_ascii=False))

        case "fetch":
            credential = auth.login_from_stored(fake=args.no_auth)
            replies = fetch_replies(
                args.bvid,
                limit=args.limit,
                credential=credential,
                sort=args.sort,
                min_likes=args.min_likes,
                start_date=args.start_date,
                end_date=args.end_date
            )
            store_replies(replies, filepath=args.output)
            print(f"Fetched {len(replies)} comments and saved to {args.output}")

        case "analyze":
            analyze_comments(
                comments_file=args.input,
                output_dir=args.output,
                start_date=args.start_date,
                end_date=args.end_date
            )
            print(f"Analysis results saved to {args.output}")

if __name__ == "__main__":
    main()