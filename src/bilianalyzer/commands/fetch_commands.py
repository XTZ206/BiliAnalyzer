import click
import asyncio
from bilibili_api import Credential
from ..auth import load_credential
from ..fetch.comments import Fetcher, save_replies, save_video_info

@click.argument('bvid',type=str)
@click.option(
    '-n', '--limit', type=int, default=10, help='Limit the maximum number of pages to fetch (default: 10)')
@click.option(
    '-o', '--output', type=str, default='comments.json', help='Output filepath  for comments (default: comments.json)')
@click.option(
    '--no-auth', is_flag=True, help='Skip authentication and fetch comments without credentials')
@click.command(help="Fetch comments for a video with given BVID\n\n"
                "POSITIONAL ARGUMENTS:\n\n"
                "BVID: Bilibili video identifier (e.g. BV1xx411c7mz)")
def fetch(bvid, limit, output, no_auth):
    """Fetch comments for a video with given BVID"""
    async def async_fetch():
        credential: Credential = Credential()
        if not no_auth:
            try:
                credential = load_credential()
            except ValueError as error:
                print(f"Authentication Failed: {error}")
                return
        fetcher = Fetcher(bvid, credential)
        replies = await fetcher.fetch_replies(limit)
        video_info = await fetcher.fetch_video_info()
        save_replies(replies, filepath=output)

        # TODO: replace hardcoded video_info filepath
        save_video_info(video_info, filepath="video_info.json")
    asyncio.run(async_fetch())
