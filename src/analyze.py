import os
import json
import matplotlib.pyplot as plt

from utils import*

def analyze_comments(
    comments_file: str,
    output_dir: str = "analysis/",
    start_date: str = None,
    end_date: str = None
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    
    # Load comments
    replies = load_replies(comments_file)
    
    # Filter comments by date
    replies = filter_comments(replies, 0, start_date, end_date)
    
    members = fetch_members(replies)
    
    # Analyze data
    sex_distribution = analyze_sexes(members)
    pendant_distribution = analyze_pendants(members)
    location_distribution = analyze_locations(replies)
    
    # Save analysis results
    with open(os.path.join(output_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump({
            "total_comments": len(replies),
            "total_users": len(members),
            "sex_distribution": dict(sex_distribution),
            "pendant_distribution": dict(pendant_distribution),
            "location_distribution": dict(location_distribution)
        }, f, ensure_ascii=False, indent=4)
    
    # Generate charts (optional)
    _generate_charts(output_dir, sex_distribution, pendant_distribution, location_distribution)

def _generate_charts(output_dir: str, sex_dist: dict, pendant_dist: dict, location_dist: dict) -> None:
    plt.rcParams['font.sans-serif'] = ['SimSun']  # Specify Chinese font (use SimSun for Windows, adjust for other systems)
    plt.rcParams['axes.unicode_minus'] = False     # Fix issue where negative signs are displayed as squares
    """Generate analysis charts"""
    # Pie chart of gender distribution
    plt.figure(figsize=(10, 5))
    plt.pie(sex_dist.values(), labels=sex_dist.keys(), autopct='%1.1f%%')
    plt.title("User Gender Distribution")
    plt.savefig(os.path.join(output_dir, "sex_distribution.png"))
    
    # Bar chart of pendant distribution
    plt.figure(figsize=(12, 6))
    top_pendants = dict(pendant_dist.most_common(10))
    plt.bar(top_pendants.keys(), top_pendants.values())
    plt.xticks(rotation=45)
    plt.title("User Pendant Distribution (Top 10)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pendant_distribution.png"))