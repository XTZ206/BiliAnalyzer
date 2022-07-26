from enum import Enum


# 字段枚举
class Fields(Enum):
    ALL = "all"
    WHOLE = "all"
    WORDS = "words"
    EMOTE = "emote"
    SEX = "sex"
    GENDER = "sex"
    LEVEL = "level"
    VIP = "vip"
    VERIFY = "verify"
    SAILINGS = "sailings"


# 字段枚举组合
SPECIAL_FIELDS = (Fields.ALL, Fields.WHOLE)  # 特殊字段 并不对应数据库中的任意字段
COMMENT_FIELDS = (Fields.WORDS, Fields.EMOTE)  # 评论字段 对应数据库Comments表中的字段
USER_FIELDS = (Fields.SEX, Fields.LEVEL, Fields.VIP, Fields.VERIFY, Fields.SAILINGS)  # 用户字段 对应数据库中Users表中的字段
USER_INFO_FIELDS = (Fields.SEX, Fields.LEVEL, Fields.VIP)  # 用户信息字段 对应数据库中SEX LEVEL VIP 三个字段
COMMON_FIELDS = COMMENT_FIELDS + USER_FIELDS  # 普通字段 对应数据库中一个确定的字段
SORTABLE_FIELDS = (Fields.WORDS, Fields.EMOTE, Fields.SEX, Fields.LEVEL, Fields.VIP, Fields.SAILINGS)  # 可排序字段

# MAIN_NAME = "Main"
# ANALYZER_NAME = "Analyze"
# PREPROCESSOR_NAME = "Preprocess"
# DOWNLOADER_NAME = "Download"
# DB_LOADER_NAME = "Load"
# DB_DUMPER_NAME = "Dump"
#
# ID_HELP = "the id of resource you want to analyze"
# ACTION_HELP = {
#     "download": "download the comments",
#     "preprocess": "preprocess the comments",
#     "analyze": "analyze the comments",
#     "all": "download, preprocess and analyze the comments"
# }
# OTYPE_HELP = {
#     "dynamic": "download dynamic comments",
#     "video": "download video comments"
# }
# OPT_HELP = {
#     "sort": "where you want to store the results",
#     "quiet": "stop logging on the screen"
# }
#
# TIMEOUT_ERROR_MSG = "Timeout Error"
# START_INFO_MSG = "Start"
# FINISH_INFO_MSG = "Finish"
# TIME_COST_MSG = "Time Cost"
# TIME_COST_UNIT = "s"

MAIN_NAME = "全局"
ANALYZER_NAME = "分析"
PREPROCESSOR_NAME = "预处理"
DOWNLOADER_NAME = "下载"
DB_LOADER_NAME = "读取"
DB_DUMPER_NAME = "存储"

ID_HELP = "输入资源ID 视频即BV号 动态即t.bilibili.com/到?的数字"
ACTION_HELP = {
    "download": "下载评论并保存",
    "preprocess": "预处理评论并保存",
    "analyze": "分析评论",
    "all": "下载 预处理 分析 全部运行"
}
OTYPE_HELP = {
    "dynamic": "指明资源类型是动态(目前只支持纯文字动态)",
    "video": "指明资源类型是视频"
}
OPT_HELP = {
    "sort": "选择日志和结果保存路径(文件夹)",
    "quiet": "停止显示日志(仍旧保存)"
}

TIMEOUT_ERROR_MSG = "超时错误"
START_INFO_MSG = "开始"
FINISH_INFO_MSG = "完成"
TIME_COST_MSG = "用时"
TIME_COST_UNIT = "秒"
