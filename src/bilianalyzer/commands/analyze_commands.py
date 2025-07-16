import click
import json
from ..analyze.comments import CommentAnalyzer, Analysis
from ..fetch.comments import load_video_info, load_replies
import asyncio


@click.argument("input", type=str)
@click.option(
    "-o",
    "--output",
    type=str,
    default="analysis_results.json",
    help="Output filepath for analysis results (default: analysis_results.json)",
)
@click.command(
    help="Analyze comments from a file\n\n"
    "POSITIONAL ARGUMENTS:\n\n"
    "INPUT: Input file with comments to analyze"
)
def analyze(input, output):
    """Analyze comments from a file"""

    async def async_analyze():
        video_info = load_video_info(filepath="video_info.json")
        replies = load_replies(filepath=input)
        analyzer = CommentAnalyzer(video_info, replies)
        analysis: Analysis = analyzer.generate_analysis()

        with open(output, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=4)

        # 命令行格式化输出分析报告
        print("=" * 40)
        print("BiliAnalyzer 评论分析报告")
        print("=" * 40)
        print(f"评论数量: {analysis.get('reply_count', 0)}")
        print(f"用户数量: {analysis.get('member_count', 0)}")
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
        print(f"共分析 {analysis['reply_count']} 条评论")
        print(f"来自 {analysis['member_count']} 位用户")

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
        print(f"分析结果已保存到 {output}")

    asyncio.run(async_analyze())
