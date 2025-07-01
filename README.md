# BiliAnalyzer

A Python-Implemented Command Line Bilibili Comment Fetch and Analysis Tool

## Install

``` shell
git clone https://github.com/XTZ206/BiliAnalyzer.git
cd BiliAnalyzer
pip install bilibili-api-python
pip install httpx
pip install matplotlib
```

## Usage

### Login With Cookies

``` shell
python src/main.py auth login
# Follow the instructions to login with cookies
# You can get the cookies from your browser
python main.py auth logout       
# 注销并删除保存的 cookies
```

### Check Login Status

``` shell
python src/main.py auth status
# Check if you are logged in
```

### Config Comments

``` shell
python src/main.py config set <key> <value>  # 设置配置项（如 output_dir, page_size）
python src/main.py config show [--key <key>] # 查看配置项（可选指定 key）
```


### Fetch Comments

``` shell
python src/main.py fetch <bvid>
  [-n/--limit <pages>]             # 最大抓取页数（默认 20）
  [-o/--output <file>]             # 输出文件路径（默认 output/comments.json）
  [--sort <time/like>]             # 排序方式（默认 time）
  [--min-likes <count>]            # 最小点赞数过滤
  [--start-date <YYYY-MM-DD>]      # 开始日期过滤
  [--end-date <YYYY-MM-DD>]        # 结束日期过滤
# make sure you have logged in first
# otherwise the file will be empty
# <bvid> is the Bilibili video ID, e.g. BV1xxxx
```

### Analyze Comments

``` shell
python src/main.py analyze <input_file>
  [-o/--output <dir>]              # 输出目录（默认 output/analysis/）
  [--start-date <YYYY-MM-DD>]      # 开始日期过滤
  [--end-date <YYYY-MM-DD>]        # 结束日期过滤
```

### Config File

配置文件位于 ~/.bili_analyzer/config.json，默认内容：
``` shell
{
  "output_dir": "output/",
  "page_size": 20,
  "sort_order": "time"
}
```
可通过 config 命令修改，或直接编辑此文件。


### Output Results

分析结果包含：
result.json：包含以下统计数据
``` shell
{
  "total_comments": 1234,
  "total_users": 567,
  "sex_distribution": {"男": 45%, "女": 30%, "保密": 25%},
  "pendant_distribution": {"会员挂件": 30%, "活动挂件": 20%, ...},
}
```
sex_distribution.png：用户性别分布饼图
pendant_distribution.png：用户装扮分布柱状图（前 10 名）