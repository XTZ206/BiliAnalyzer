"""
重定位图片路径
"""
import sys

filepath = sys.argv[1]
with open(filepath, "r", encoding="utf-8") as f:
    file_content = f.read()
with open(filepath, "w", encoding="utf-8") as f:
    f.write(file_content.replace("../icon/", "./icon/"))

