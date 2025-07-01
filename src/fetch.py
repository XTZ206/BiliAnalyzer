import time
from bilibili_api import Credential, bvid2aid, sync
from bilibili_api.comment import CommentResourceType, get_comments, OrderType
from typing import List, Dict, Optional

from utils import Reply, filter_comments

def fetch_replies(
    bvid: str,
    limit: int = 20,
    credential: Optional[Credential] = None,
    sort: str = "time",
    min_likes: int = 0,
    start_date: str = None,
    end_date: str = None
) -> List[Reply]:
    #Fetch video comments with filtering suppor
    # Set sorting method based on the 'sort' parameter (modified to use CommentSortOrder enum)
    order_type = OrderType.TIME if sort == "time" else OrderType.LIKE
    
    # Modification: Use CommentSortOrder enum type
    page: Dict = sync(get_comments(
        bvid2aid(bvid), 
        CommentResourceType.VIDEO, 
        credential=credential, 
        order=order_type  # Now passing enum type
    ))
    
    count: int = page.get("page", {}).get("count", 0)
    index: int = 1
    replies: List[Reply] = []

    for reply in page.get("replies", []):
        replies.append(reply)
        for reply in reply.get("replies", []):
            replies.append(reply)

    # Apply initial filtering
    replies = filter_comments(replies, min_likes, start_date, end_date)
    
    while limit == 0 or index < limit:
        if len(replies) >= count or page.get("replies") == []:
            break
        index += 1
        
        # Modification: Use CommentSortOrder enum type
        page: Dict = sync(get_comments(
            bvid2aid(bvid), 
            CommentResourceType.VIDEO, 
            page_index=index, 
            credential=credential, 
            order=order_type  # Now passing enum type
        ))
        
        time.sleep(1)
        
        new_replies = []
        for reply in page.get("replies", []):
            new_replies.append(reply)
            for reply in reply.get("replies", []):
                new_replies.append(reply)
        
        # Filter new comments
        new_replies = filter_comments(new_replies, min_likes, start_date, end_date)
        replies.extend(new_replies)

    return replies