# BiliAnalyzer

A Python-Implemented Command Line Bilibili Comment Fetch and Analysis Tool

## Install

``` shell
git clone https://github.com/XTZ206/BiliAnalyzer.git
cd BiliAnalyzer
pip install bilibili-api-python
pip install httpx
```

## Usage

### Login With Cookies

``` shell
python src/main.py auth login
# Follow the instructions to login with cookies
# You can get the cookies from your browser
```

### Check Login Status

``` shell
python src/main.py auth status
# Check if you are logged in
```

### Fetch Comments

``` shell
python src/main.py fetch <bvid> [-o <path/to/comments.json>]
# make sure you have logged in first
# otherwise the file will be empty
# <bvid> is the Bilibili video ID, e.g. BV1xxxx
```

### Analyze Comments

``` shell
python src/main.py analyze <path/to/comments.json> [-o <path/to/analysis_results.json>]
```
