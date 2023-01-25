# BiliAnalyzer

哔哩哔哩成分查询机，支持下载视频评论并分析成分

## 使用指南

### 二进制版本

[下载](https://github.com/XTZ206/BiliAnalyzer/releases)最新版本压缩包后
解压至文件夹并双击BiliAnalyzer.exe运行

### 源代码运行

克隆或[下载](https://github.com/XTZ206/BiliAnalyzer/archive/main.zip)本代码仓库
并使用pip安装依赖
启动脚本

```commandline
git clone https://github.com/XTZ206/BiliAnalyzer.git
cd .\BiliAnalyzer
pip install -r requirements.txt
python bilianalyzer\bilibili.py
```

### 自行编译

使用pip安装Pyinstaller后 BiliAnalyzer.spec作为配置文件编译

```commandline
pyinstaller BiliAnalyzer.spec
```

## 开源协议

BiliAnalyzer is under GNU General Public License version 3.0

本项目基于GPLv3发布
