import click
import asyncio
import json

from bilibili_api import Credential
from .commands import auth_commands
from .fetch.comments import (
    Fetcher,
    save_replies,
    load_replies,
    save_video_info,
    load_video_info,
)
from .analyze.comments import CommentAnalyzer, save_analysis
from .utils import *

@click.group()
def main():
    """BiliAnalyzer: Fetch and Analyze Bilibili Comments"""
    
main.add_command(auth_commands.auth)

if __name__ == "__main__":
    main()
